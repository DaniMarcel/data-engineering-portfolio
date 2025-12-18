# ☁️ AWS S3 con LocalStack

Desarrollo local de AWS S3 con LocalStack.

**Setup:**

```bash
docker run -p 4566:4566 localstack/localstack
pip install -r requirements.txt
python src/s3_client.py
```

**Features:**

- Create buckets
- Upload/download files
- List objects
- Local development sin AWS account

**LocalStack** simula AWS services locally.
