"""Azure Blob Storage Client Simulation"""
from datetime import datetime

class AzureBlobClient:
    """Simulates Azure Blob Storage operations"""
    
    def __init__(self, account_name, container_name):
        self.account_name = account_name
        self.container_name = container_name
        self.blobs = {}
        print(f"📦 Connected to Azure Storage Account: {account_name}")
        print(f"   Container: {container_name}")
    
    def upload_blob(self, blob_name, data):
        """Upload data to blob"""
        self.blobs[blob_name] = {
            'data': data,
            'size': len(str(data)),
            'uploaded_at': datetime.now(),
            'content_type': 'application/octet-stream'
        }
        print(f"✅ Uploaded blob: {blob_name} ({self.blobs[blob_name]['size']} bytes)")
    
    def download_blob(self, blob_name):
        """Download blob data"""
        if blob_name not in self.blobs:
            print(f"❌ Blob not found: {blob_name}")
            return None
        
        print(f"📥 Downloaded blob: {blob_name}")
        return self.blobs[blob_name]['data']
    
    def list_blobs(self):
        """List all blobs"""
        print(f"\n📋 Blobs in container '{self.container_name}':")
        for name, info in self.blobs.items():
            print(f"  - {name} ({info['size']} bytes) - {info['uploaded_at']}")
        return list(self.blobs.keys())

# Example usage
if __name__ == '__main__':
    print("☁️  AZURE BLOB STORAGE EXAMPLE\n")
    
    # Create client
    client = AzureBlobClient('mystorageaccount', 'data-container')
    
    # Upload files
    client.upload_blob('sales_data.csv', 'id,amount,date\n1,100,2024-01-01')
    client.upload_blob('customers.json', '{"customers": []}')
    client.upload_blob('processed/output.parquet', b'binary_data_here')
    
    # List blobs
    client.list_blobs()
    
    # Download
    data = client.download_blob('sales_data.csv')
    print(f"\n📄 Downloaded content preview:\n{data[:50]}...")
    
    print("\n✅ Azure Blob Storage operations completed!")
