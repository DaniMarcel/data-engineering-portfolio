"""LocalStack S3 - Cloud Storage Local"""
import boto3
from botocore.config import Config

# LocalStack configuration
def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url='http://localhost:4566',
        aws_access_key_id='test',
        aws_secret_access_key='test',
        region_name='us-east-1',
        config=Config(signature_version='s3v4')
    )

def create_bucket(bucket_name):
    s3 = get_s3_client()
    s3.create_bucket(Bucket=bucket_name)
    print(f"✅ Bucket created: {bucket_name}")

def upload_file(bucket_name, file_path, object_name):
    s3 = get_s3_client()
    s3.upload_file(file_path, bucket_name, object_name)
    print(f"✅ Uploaded: {object_name}")

def list_files(bucket_name):
    s3 = get_s3_client()
    response = s3.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        for obj in response['Contents']:
            print(f"📄 {obj['Key']} - {obj['Size']} bytes")

if __name__ == "__main__":
    print("🌩️  LocalStack S3 Example")
    print("Make sure LocalStack is running: docker run -p 4566:4566 localstack/localstack")
    
    BUCKET = 'data-engineering-bucket'
    
    try:
        create_bucket(BUCKET)
        print(f"\n📊 Bucket: {BUCKET}")
    except Exception as e:
        print(f"⚠️  LocalStack not running or bucket exists: {e}")
