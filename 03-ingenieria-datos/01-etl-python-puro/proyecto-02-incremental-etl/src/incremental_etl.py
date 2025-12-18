"""Incremental ETL - Only process new/changed records"""
import pandas as pd
from pathlib import Path
from datetime import datetime
import json

class IncrementalETL:
    def __init__(self, checkpoint_file='checkpoint.json'):
        self.checkpoint_file = Path(checkpoint_file)
        self.checkpoint = self.load_checkpoint()
    
    def load_checkpoint(self):
        if self.checkpoint_file.exists():
            with open(self.checkpoint_file) as f:
                return json.load(f)
        return {'last_run': None, 'last_id': 0}
    
    def save_checkpoint(self):
        with open(self.checkpoint_file, 'w') as f:
            json.dump(self.checkpoint, f)
    
    def extract_new(self, df):
        """Extract only new records"""
        last_id = self.checkpoint['last_id']
        
        # Extract numeric portion from string IDs like 'T000001'
        df['_numeric_id'] = df['transaccion_id'].str.extract(r'(\d+)')[0].astype(int)
        
        new_records = df[df['_numeric_id'] > last_id].copy()
        print(f"📥 New records: {len(new_records)} (since ID {last_id})")
        return new_records
    
    def transform(self, df):
        """Transform data"""
        df_clean = df.dropna()
        print(f"🔄 Transformed: {len(df_clean)} records")
        return df_clean
    
    def load(self, df, output_path):
        """Append to existing data"""
        output_path = Path(output_path)
        
        if output_path.exists():
            existing = pd.read_parquet(output_path)
            combined = pd.concat([existing, df], ignore_index=True)
        else:
            combined = df
        
        combined.to_parquet(output_path)
        print(f"💾 Total records: {len(combined)}")
        
        # Update checkpoint with numeric ID
        self.checkpoint['last_id'] = int(df['_numeric_id'].max())
        self.checkpoint['last_run'] = datetime.now().isoformat()
        self.save_checkpoint()
        print(f"📝 Checkpoint updated: last_id = {self.checkpoint['last_id']}")
    
    def run(self, source_path, output_path):
        print(f"📂 Loading data from: {source_path}")
        
        if not Path(source_path).exists():
            print(f"❌ File not found: {source_path}")
            return
        
        df = pd.read_csv(source_path)
        print(f"📊 Total records in source: {len(df)}")
        print(f"   Column 'transaccion_id' exists: {'transaccion_id' in df.columns}")
        
        if 'transaccion_id' in df.columns:
            print(f"   Sample IDs: {df['transaccion_id'].head().tolist()}")
        
        new_df = self.extract_new(df)
        
        if len(new_df) > 0:
            transformed = self.transform(new_df)
            self.load(transformed, output_path)
            print("✅ Incremental ETL completed")
        else:
            print("ℹ️  No new records to process")

if __name__ == "__main__":
    print("🔄 ETL INCREMENTAL\n")
    
    etl = IncrementalETL()
    
    # Buscar carpeta base 'data engineer'
    current_path = Path(__file__).resolve()
    base_path = None
    for parent in current_path.parents:
        if parent.name == 'data engineer':
            base_path = parent
            break
    
    if base_path is None:
        raise FileNotFoundError("No se pudo encontrar la carpeta base 'data engineer'")
    
    source = base_path / '02-analisis-datos' / '01-eda-exploratorio' / 'proyecto-01-ventas-retail' / 'data' / 'raw' / 'transacciones.csv'
    output = Path('output/incremental_data.parquet')
    output.parent.mkdir(exist_ok=True)
    
    etl.run(source, output)
