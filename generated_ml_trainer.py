"""
Machine Learning Model Trainer

Generated: 2025-11-26 09:00:17
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
from typing import Tuple

class ModelTrainer:
    """
    Train and manage ML models.
    
    Attributes:
        model (RandomForestClassifier): ML model
        feature_names (list): Feature names
    """
    
    def __init__(self, model: RandomForestClassifier, feature_names: list = '[]'):
        """Initialize ModelTrainer."""
        self.model = model
        self.feature_names = feature_names


    def load_data(self: , csv_path: str) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Load and prepare data.
        
        Args:
            self (): 
            csv_path (str): 
        
        Returns:
            Tuple[pd.DataFrame, pd.Series]
        """
        df = pd.read_csv(csv_path)
        print(f'Loaded {len(df)} samples')

        # Separate features and target
        X = df.drop('target', axis=1)
        y = df['target']

        self.feature_names = X.columns.tolist()

        return X, y

    def train(self: , X: pd.DataFrame, y: pd.Series, test_size: float = 0.2) -> Dict:
        """
        Train the model.
        
        Args:
            self (): 
            X (pd.DataFrame): 
            y (pd.Series): 
            test_size (float): 
        
        Returns:
            Dict
        """
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )

        print(f'Training on {len(X_train)} samples...')

        # Train model
        self.model.fit(X_train, y_train)

        # Evaluate
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        print(f'Accuracy: {accuracy:.3f}')

        return {
            'accuracy': accuracy,
            'train_size': len(X_train),
            'test_size': len(X_test)
        }

    def predict(self: , X: pd.DataFrame) -> np.ndarray:
        """
        Make predictions.
        
        Args:
            self (): 
            X (pd.DataFrame): 
        
        Returns:
            np.ndarray
        """
        return self.model.predict(X)

    def save(self: , path: str) -> None:
        """
        Save model to disk.
        
        Args:
            self (): 
            path (str): 
        
        Returns:
            None
        """
        joblib.dump(self.model, path)
        print(f'Model saved to {path}')



if __name__ == '__main__':

    # Initialize trainer
    trainer = ModelTrainer(
        model=RandomForestClassifier(n_estimators=100, random_state=42)
    )

    # Load and train
    X, y = trainer.load_data('data.csv')
    metrics = trainer.train(X, y)

    print(f"Training complete!")
    print(f"- Accuracy: {metrics['accuracy']:.3f}")
    print(f"- Train samples: {metrics['train_size']}")
    print(f"- Test samples: {metrics['test_size']}")

    # Save model
    trainer.save('model.pkl')