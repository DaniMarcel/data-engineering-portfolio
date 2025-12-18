# ✅ Validación de Datos con Pydantic

## 🎯 Objetivos

- ✅ Validación robusta con **Pydantic v2**
- ✅ Type hints y validación automática
- ✅ Validadores personalizados
- ✅ Mensajes de error claros
- ✅ Validación en lote

## 🚀 Quick Start

```bash
pip install -r requirements.txt
cd src
python validador.py
```

## 📋 Modelos Incluidos

- **Usuario**: Email, edad (18-120), campos requeridos
- **Dirección**: Código postal regex, validación de formato
- **Producto**: SKU pattern, precio razonable, nombre capitalizado
- **Transacción**: Validación de total calculado, descuentos

## 💡 Características

- Field validators personalizados
- Root validators para validación entre campos
- Regex patterns para formatos
- Constrained types (gt, ge, min_length, etc.)
- Literal types para enums

## 🎓 Conceptos

- Type hints de Python
- Decorador @validator
- @root_validator para múltiples campos
- model_dump() para serialización
- Mensajes de error descriptivos

---

Pydantic es el estándar para validación de datos en Python moderno.
