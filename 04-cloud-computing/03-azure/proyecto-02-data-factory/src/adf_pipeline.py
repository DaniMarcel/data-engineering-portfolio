"""Azure Data Factory Pipeline Simulation"""
from datetime import datetime
import json

class AzureDataFactory:
    """Simulates Azure Data Factory pipeline"""
    
    def __init__(self, factory_name):
        self.factory_name = factory_name
        self.pipelines = {}
    
    def create_pipeline(self, name, activities):
        """Create a data pipeline"""
        self.pipelines[name] = {
            'name': name,
            'activities': activities,
            'created': datetime.now()
        }
        print(f"✅ Pipeline '{name}' created")
    
    def run_pipeline(self, name):
        """Execute pipeline"""
        if name not in self.pipelines:
            print(f"❌ Pipeline '{name}' not found")
            return
        
        pipeline = self.pipelines[name]
        print(f"\n🚀 Running pipeline: {name}")
        
        for activity in pipeline['activities']:
            print(f"  ▶ Executing: {activity['name']} ({activity['type']})")
            if activity['type'] == 'Copy':
                print(f"    Source: {activity['source']}")
                print(f"    Sink: {activity['sink']}")
            elif activity['type'] == 'DataFlow':
                print(f"    Transforming data...")
        
        print(f"✅ Pipeline '{name}' completed\n")

# Example usage
if __name__ == '__main__':
    print("☁️  AZURE DATA FACTORY SIMULATION\n")
    
    adf = AzureDataFactory('MyDataFactory')
    
    # Define pipeline
    pipeline_activities = [
        {
            'name': 'CopyFromBlob',
            'type': 'Copy',
            'source': 'AzureBlobStorage',
            'sink': 'AzureSQLDatabase'
        },
        {
            'name': 'TransformData',
            'type': 'DataFlow',
            'transformation': 'CleanAndAggregate'
        },
        {
            'name': 'LoadToWarehouse',
            'type': 'Copy',
            'source': 'AzureSQLDatabase',
            'sink': 'Synapse'
        }
    ]
    
    adf.create_pipeline('ETL_Pipeline', pipeline_activities)
    adf.run_pipeline('ETL_Pipeline')
    
    print("📊 Pipeline Summary:")
    print(f"  Factory: {adf.factory_name}")
    print(f"  Pipelines: {len(adf.pipelines)}")
    print("\n✅ Azure Data Factory simulation completed!")
