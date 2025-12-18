"""AWS Lambda ETL Simulation"""
# Simulates AWS Lambda function for ETL

import json
from datetime import datetime

def lambda_handler(event, context):
    """
    AWS Lambda handler for ETL processing
    
    Args:
        event: Input event data
        context: Lambda context
    """
    print(f"🔥 Lambda function triggered at {datetime.now()}")
    
    # Extract
    records = event.get('records', [])
    print(f"📥 Extracting {len(records)} records")
    
    # Transform
    transformed = []
    for record in records:
        transformed_record = {
            'id': record.get('id'),
            'value': record.get('value', 0) * 2,
            'processed_at': datetime.now().isoformat(),
            'status': 'processed'
        }
        transformed.append(transformed_record)
    
    print(f"🔄 Transformed {len(transformed)} records")
    
    # Load (simulate)
    print(f"💾 Loading to S3/DynamoDB...")
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'ETL completed successfully',
            'records_processed': len(transformed),
            'timestamp': datetime.now().isoformat()
        })
    }

# Local testing
if __name__ == '__main__':
    print("🧪 Testing Lambda function locally\n")
    
    # Simulate event
    test_event = {
        'records': [
            {'id': 1, 'value': 100},
            {'id': 2, 'value': 200},
            {'id': 3, 'value': 300}
        ]
    }
    
    result = lambda_handler(test_event, None)
    print(f"\n✅ Result: {json.dumps(result, indent=2)}")
