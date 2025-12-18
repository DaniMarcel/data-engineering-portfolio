"""Luigi Data Pipeline Example"""
import luigi
from pathlib import Path

class ExtractData(luigi.Task):
    """Extract data task"""
    
    def output(self):
        return luigi.LocalTarget('data/raw_data.txt')
    
    def run(self):
        with self.output().open('w') as f:
            f.write("Sample data extracted\n")
            f.write("Record 1, Record 2, Record 3\n")
        print("✅ Data extracted")

class TransformData(luigi.Task):
    """Transform data task"""
    
    def requires(self):
        return ExtractData()
    
    def output(self):
        return luigi.LocalTarget('data/transformed_data.txt')
    
    def run(self):
        with self.input().open('r') as infile:
            data = infile.read()
        
        transformed = data.upper()
        
        with self.output().open('w') as outfile:
            outfile.write(transformed)
        
        print("✅ Data transformed")

class LoadData(luigi.Task):
    """Load data task"""
    
    def requires(self):
        return TransformData()
    
    def output(self):
        return luigi.LocalTarget('data/final_output.txt')
    
    def run(self):
        with self.input().open('r') as infile:
            data = infile.read()
        
        with self.output().open('w') as outfile:
            outfile.write(f"FINAL: {data}")
        
        print("✅ Data loaded")

if __name__ == '__main__':
    luigi.build([LoadData()], local_scheduler=True)
    print("🎉 Pipeline completed!")
