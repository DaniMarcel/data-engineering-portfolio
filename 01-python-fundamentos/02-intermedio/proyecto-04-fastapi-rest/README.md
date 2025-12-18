# 🚀 FastAPI REST API

API REST para servir datos.

**Start:**

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload
```

**Endpoints:**

- GET / - Info
- GET /health - Health check
- GET /api/transactions - Get transactions
- GET /api/stats - Statistics

**Docs:** http://localhost:8000/docs (Swagger UI automático)

FastAPI genera documentación OpenAPI automáticamente.
