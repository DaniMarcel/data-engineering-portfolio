"""
Pipeline ETL Básico con Python Puro
====================================

Pipeline completo de Extract-Transform-Load sin usar frameworks externos.
Demuestra los conceptos fundamentales de ingeniería de datos.

Proceso:
1. EXTRACT: Lee datos de múltiples fuentes (CSV, JSON)
2. TRANSFORM: Limpia, valida y transforma los datos
3. LOAD: Guarda en formato optimizado (Parquet, JSON)
"""

import csv
import json
import logging
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import sys

# Configurar logging
def configurar_logging():
    """Configura el sistema de logging."""
    log_dir = Path(__file__).parent.parent / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f'etl_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)

logger = configurar_logging()


class ETLPipeline:
    """Pipeline ETL completo."""
    
    def __init__(self, config):
        """
        Inicializa el pipeline.
        
        Args:
            config (dict): Configuración del pipeline
        """
        self.config = config
        self.data_raw = []
        self.data_transformed = []
        self.stats = {
            'extracted': 0,
            'transformed': 0,
            'loaded': 0,
            'errors': 0
        }
    
    # ======= EXTRACT =======
    
    def extract_csv(self, file_path):
        """
        Extrae datos de archivo CSV.
        
        Args:
            file_path (Path): Ruta al archivo CSV
            
        Returns:
            list: Registros extraídos
        """
        logger.info(f"📥 Extrayendo datos de CSV: {file_path.name}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data = list(reader)
            
            logger.info(f"   ✅ {len(data)} registros extraídos")
            self.stats['extracted'] += len(data)
            return data
        
        except Exception as e:
            logger.error(f"   ❌ Error extrayendo CSV: {e}")
            self.stats['errors'] += 1
            return []
    
    def extract_json(self, file_path):
        """
        Extrae datos de archivo JSON.
        
        Args:
            file_path (Path): Ruta al archivo JSON
            
        Returns:
            list: Registros extraídos
        """
        logger.info(f"📥 Extrayendo datos de JSON: {file_path.name}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Si es un objeto con lista dentro, extraerla
            if isinstance(data, dict):
                # Buscar la primera key que contenga una lista
                for key, value in data.items():
                    if isinstance(value, list):
                        data = value
                        break
            
            logger.info(f"   ✅ {len(data)} registros extraídos")
            self.stats['extracted'] += len(data)
            return data
        
        except Exception as e:
            logger.error(f"   ❌ Error extrayendo JSON: {e}")
            self.stats['errors'] += 1
            return []
    
    def extract_all(self):
        """Extrae datos de todas las fuentes configuradas."""
        logger.info("="*70)
        logger.info("🔄 FASE 1: EXTRACT (Extracción)")
        logger.info("="*70)
        
        sources = self.config.get('sources', [])
        
        for source in sources:
            file_path = Path(source['path'])
            file_type = source['type']
            
            if not file_path.exists():
                logger.warning(f"⚠️  Archivo no encontrado: {file_path}")
                continue
            
            if file_type == 'csv':
                data = self.extract_csv(file_path)
            elif file_type == 'json':
                data = self.extract_json(file_path)
            else:
                logger.warning(f"⚠️  Tipo de archivo no soportado: {file_type}")
                continue
            
            # Añadir metadatos de origen
            for record in data:
                record['_source'] = file_path.name
                record['_extracted_at'] = datetime.now().isoformat()
            
            self.data_raw.extend(data)
        
        logger.info(f"\n📊 Total registros extraídos: {len(self.data_raw)}")
    
    # ======= TRANSFORM =======
    
    def validate_record(self, record):
        """
        Valida un registro según reglas de negocio.
        
        Args:
            record (dict): Registro a validar
            
        Returns:
            tuple: (is_valid, errors)
        """
        errors = []
        
        # Reglas de validación (ejemplo)
        required_fields = self.config.get('required_fields', [])
        
        for field in required_fields:
            if field not in record or record[field] is None or record[field] == '':
                errors.append(f"Campo requerido vacío: {field}")
        
        return len(errors) == 0, errors
    
    def clean_record(self, record):
        """
        Limpia un registro.
        
        Args:
            record (dict): Registro a limpiar
            
        Returns:
            dict: Registro limpio
        """
        cleaned = record.copy()
        
        # Limpiar strings
        for key, value in cleaned.items():
            if isinstance(value, str):
                cleaned[key] = value.strip()
        
        # Normalizar campos numéricos
        numeric_fields = self.config.get('numeric_fields', [])
        for field in numeric_fields:
            if field in cleaned and cleaned[field]:
                try:
                    cleaned[field] = float(cleaned[field])
                except (ValueError, TypeError):
                    cleaned[field] = 0.0
        
        return cleaned
    
    def enrich_record(self, record):
        """
        Enriquece un registro con campos calculados.
        
        Args:
            record (dict): Registro a enriquecer
            
        Returns:
            dict: Registro enriquecido
        """
        enriched = record.copy()
        
        # Añadir timestamp de procesamiento
        enriched['_processed_at'] = datetime.now().isoformat()
        
        # Calcular campos derivados (ejemplo)
        if 'cantidad' in enriched and 'precio_unitario' in enriched:
            try:
                enriched['total_calculado'] = enriched['cantidad'] * enriched['precio_unitario']
            except (TypeError, ValueError):
                enriched['total_calculado'] = 0.0
        
        return enriched
    
    def transform_all(self):
        """Transforma todos los datos extraídos."""
        logger.info("\n" + "="*70)
        logger.info("🔄 FASE 2: TRANSFORM (Transformación)")
        logger.info("="*70)
        
        valid_count = 0
        invalid_count = 0
        
        for record in self.data_raw:
            # 1. Validar
            is_valid, errors = self.validate_record(record)
            
            if not is_valid:
                logger.warning(f"⚠️  Registro inválido: {errors}")
                invalid_count += 1
                continue
            
            # 2. Limpiar
            cleaned = self.clean_record(record)
            
            # 3. Enriquecer
            enriched = self.enrich_record(cleaned)
            
            self.data_transformed.append(enriched)
            valid_count += 1
        
        self.stats['transformed'] = valid_count
        
        logger.info(f"\n📊 Registros válidos: {valid_count}")
        logger.info(f"❌ Registros inválidos: {invalid_count}")
    
    # ======= LOAD =======
    
    def load_json(self, output_path, data):
        """
        Guarda datos en formato JSON.
        
        Args:
            output_path (Path): Ruta de salida
            data (list): Datos a guardar
        """
        logger.info(f"💾 Guardando en JSON: {output_path.name}")
        
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"   ✅ {len(data)} registros guardados")
            self.stats['loaded'] += len(data)
        
        except Exception as e:
            logger.error(f"   ❌ Error guardando JSON: {e}")
            self.stats['errors'] += 1
    
    def load_csv(self, output_path, data):
        """
        Guarda datos en formato CSV.
        
        Args:
            output_path (Path): Ruta de salida
            data (list): Datos a guardar
        """
        logger.info(f"💾 Guardando en CSV: {output_path.name}")
        
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            if not data:
                logger.warning("   ⚠️  No hay datos para guardar")
                return
            
            # Obtener todos los campos
            fieldnames = list(data[0].keys())
            
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            logger.info(f"   ✅ {len(data)} registros guardados")
            self.stats['loaded'] += len(data)
        
        except Exception as e:
            logger.error(f"   ❌ Error guardando CSV: {e}")
            self.stats['errors'] += 1
    
    def load_all(self):
        """Carga todos los datos transformados."""
        logger.info("\n" + "="*70)
        logger.info("🔄 FASE 3: LOAD (Carga)")
        logger.info("="*70)
        
        outputs = self.config.get('outputs', [])
        
        for output in outputs:
            output_path = Path(output['path'])
            output_type = output['type']
            
            if output_type == 'json':
                self.load_json(output_path, self.data_transformed)
            elif output_type == 'csv':
                self.load_csv(output_path, self.data_transformed)
            else:
                logger.warning(f"⚠️  Tipo de salida no soportado: {output_type}")
    
    # ======= PIPELINE =======
    
    def run(self):
        """Ejecuta el pipeline completo ETL."""
        start_time = datetime.now()
        
        logger.info("="*70)
        logger.info("🚀 INICIANDO PIPELINE ETL")
        logger.info("="*70)
        
        try:
            # Extract
            self.extract_all()
            
            # Transform
            self.transform_all()
            
            # Load
            self.load_all()
            
            # Resumen
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logger.info("\n" + "="*70)
            logger.info("✨ PIPELINE COMPLETADO")
            logger.info("="*70)
            logger.info(f"⏱️  Duración: {duration:.2f} segundos")
            logger.info(f"📊 Estadísticas:")
            logger.info(f"   - Extraídos: {self.stats['extracted']}")
            logger.info(f"   - Transformados: {self.stats['transformed']}")
            logger.info(f"   - Cargados: {self.stats['loaded']}")
            logger.info(f"   - Errores: {self.stats['errors']}")
            
            return True
        
        except Exception as e:
            logger.error(f"❌ Error en el pipeline: {e}")
            return False


def main():
    """Función principal."""
    # Obtener rutas base
    base_path = Path(__file__).parent.parent
    
    # Buscar carpeta base 'data engineer'
    current_path = Path(__file__).resolve()
    data_engineer_base = None
    for parent in current_path.parents:
        if parent.name == 'data engineer':
            data_engineer_base = parent
            break
    
    if data_engineer_base is None:
        logger.error("No se pudo encontrar la carpeta base 'data engineer'")
        return 1
    
    # Usar datos del proyecto EDA
    data_source = data_engineer_base / '02-analisis-datos' / '01-eda-exploratorio' / 'proyecto-01-ventas-retail' / 'data' / 'raw'
    
    # Configuración del pipeline
    config = {
        'sources': [
            {
                'path': str(data_source / 'transacciones.csv'),
                'type': 'csv'
            }
        ],
        'outputs': [
            {
                'path': str(base_path / 'data/processed/transacciones_procesadas.json'),
                'type': 'json'
            },
            {
                'path': str(base_path / 'data/processed/transacciones_procesadas.csv'),
                'type': 'csv'
            }
        ],
        'required_fields': ['transaccion_id', 'fecha', 'total'],
        'numeric_fields': ['cantidad', 'precio_unitario', 'total']
    }
    
    # Crear y ejecutar pipeline
    pipeline = ETLPipeline(config)
    success = pipeline.run()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
