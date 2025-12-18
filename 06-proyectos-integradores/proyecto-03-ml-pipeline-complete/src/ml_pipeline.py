"""Complete ML Pipeline - Training, Serving, Monitoring"""
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import pickle
from datetime import datetime
from pathlib import Path

class MLPipeline:
    """End-to-end ML pipeline"""
    
    def __init__(self, model_name):
        self.model_name = model_name
        self.model = None
        self.metrics = {}
        self.predictions_log = []
    
    def train(self, X, y):
        """Train model"""
        print(f"🎯 Training model: {self.model_name}")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        self.model = LinearRegression()
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        self.metrics = {
            'r2_score': r2_score(y_test, y_pred),
            'rmse': mean_squared_error(y_test, y_pred, squared=False),
            'trained_at': datetime.now(),
            'train_size': len(X_train),
            'test_size': len(X_test)
        }
        
        print(f"  R² Score: {self.metrics['r2_score']:.4f}")
        print(f"  RMSE: {self.metrics['rmse']:.2f}")
    
    def save_model(self, path='model.pkl'):
        """Save trained model"""
        with open(path, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"💾 Model saved to {path}")
    
    def predict(self, X):
        """Make predictions"""
        predictions = self.model.predict(X)
        
        # Log for monitoring
        self.predictions_log.append({
            'timestamp': datetime.now(),
            'num_predictions': len(predictions),
            'mean_prediction': predictions.mean()
        })
        
        return predictions
    
    def monitor(self):
        """Monitor model performance"""
        print(f"\n📊 MODEL MONITORING - {self.model_name}")
        print(f"\nTraining Metrics:")
        print(f"  R² Score: {self.metrics['r2_score']:.4f}")
        print(f"  RMSE: {self.metrics['rmse']:.2f}")
        print(f"  Trained: {self.metrics['trained_at']}")
        
        print(f"\nPrediction Stats:")
        print(f"  Total prediction calls: {len(self.predictions_log)}")
        if self.predictions_log:
            print(f"  Last prediction: {self.predictions_log[-1]['timestamp']}")

# Demo
if __name__ == '__main__':
    print("🤖 COMPLETE ML PIPELINE\n")
    
    # Load data
    # Buscar carpeta base 'data engineer'

    current_path = Path(__file__).resolve()

    base_path = None

    for parent in current_path.parents:

        if parent.name == 'data engineer':

            base_path = parent

            break

    if base_path is None:

        raise FileNotFoundError("No se pudo encontrar la carpeta base 'data engineer'")
    data_path = base_path / '02-analisis-datos' / '01-eda-exploratorio' / 'proyecto-01-ventas-retail' / 'data' / 'raw' / 'transacciones.csv'
    
    if data_path.exists():
        df = pd.read_csv(data_path)
        
        # Prepare features
        X = df[['cantidad', 'precio_unitario']]
        y = df['total']
        
        # Initialize pipeline
        pipeline = MLPipeline('SalesPredictor')
        
        # Train
        pipeline.train(X, y)
        
        # Save
        pipeline.save_model('sales_model.pkl')
        
        # Predict
        test_data = [[2, 100], [5, 200]]
        predictions = pipeline.predict(test_data)
        print(f"\n🔮 Predictions: {predictions}")
        
        # Monitor
        pipeline.monitor()
        
        print("\n✅ ML Pipeline completed!")
    else:
        print("⚠️  Data not found. Using sample data.")
        X = [[1, 100], [2, 200], [3, 150], [4, 300]]
        y = [100, 400, 450, 1200]
        
        pipeline = MLPipeline('SampleModel')
        pipeline.train(pd.DataFrame(X), pd.Series(y))
        pipeline.monitor()
