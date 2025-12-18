"""GCP Dataflow Pipeline Example"""
# Apache Beam pipeline for batch/stream processing

class DataflowPipeline:
    """Simulates GCP Dataflow (Apache Beam) pipeline"""
    
    def __init__(self, pipeline_name):
        self.pipeline_name = pipeline_name
        self.steps = []
    
    def read(self, source):
        """Read from source"""
        self.steps.append(('Read', source))
        print(f"📥 Read from: {source}")
        return self
    
    def transform(self, transformation):
        """Apply transformation"""
        self.steps.append(('Transform', transformation))
        print(f"🔄 Transform: {transformation}")
        return self
    
    def write(self, sink):
        """Write to sink"""
        self.steps.append(('Write', sink))
        print(f"💾 Write to: {sink}")
        return self
    
    def run(self):
        """Execute pipeline"""
        print(f"\n🚀 Running Dataflow pipeline: {self.pipeline_name}")
        print(f"   Steps: {len(self.steps)}")
        
        for i, (step_type, detail) in enumerate(self.steps, 1):
            print(f"   {i}. {step_type}: {detail}")
        
        print(f"\n✅ Pipeline '{self.pipeline_name}' completed!")

# Example usage
if __name__ == '__main__':
    print("🌊 GCP DATAFLOW PIPELINE\n")
    
    # Batch pipeline
    batch_pipeline = DataflowPipeline('BatchETL')
    batch_pipeline \
        .read('gs://my-bucket/input/*.csv') \
        .transform('Parse CSV') \
        .transform('Filter invalid records') \
        .transform('Aggregate by key') \
        .write('bigquery://project.dataset.table') \
        .run()
    
    print("\n" + "="*60 + "\n")
    
    # Streaming pipeline
    stream_pipeline = DataflowPipeline('StreamProcessing')
    stream_pipeline \
        .read('pubsub://project/subscription') \
        .transform('Parse JSON') \
        .transform('Windowed aggregation (1 min)') \
        .write('bigquery://project.dataset.realtime_table') \
        .run()
    
    print("\n" + "="*60)
    print("Apache Beam = Unified batch + stream processing")
