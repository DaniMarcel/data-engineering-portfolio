# 🧪 Testing con Pytest

Suite de tests para funciones de data engineering.

## Quick Start

```bash
pip install -r requirements.txt
pytest tests/ -v
pytest tests/ --cov  # Con coverage
```

## Tests Incluidos

- Validación de emails
- Cálculo de edades
- Limpieza de DataFrames
- Cálculo de descuentos
- Fixtures reutilizables
- Tests parametrizados

## Comandos

```bash
pytest tests/test_funciones.py -v  # Verbose
pytest tests/ -k "email"  # Solo tests de email
pytest tests/ --markers  # Ver markers
```

---

Testing asegura calidad y previene regresiones.
