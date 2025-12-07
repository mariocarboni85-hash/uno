"""
ETL Data Pipeline

Generated: 2025-11-26 09:00:17
"""

import pandas as pd
import json
from typing import Dict, List
from pathlib import Path

class DataPipeline:
    """
    ETL pipeline for data processing.
    
    Attributes:
        input_dir (Path): Input directory
        output_dir (Path): Output directory
    """
    
    def __init__(self, input_dir: Path, output_dir: Path):
        """Initialize DataPipeline."""
        self.input_dir = input_dir
        self.output_dir = output_dir


    def extract(self: , filename: str) -> pd.DataFrame:
        """
        Extract data from CSV.
        
        Args:
            self (): 
            filename (str): 
        
        Returns:
            pd.DataFrame
        """
        file_path = self.input_dir / filename
        df = pd.read_csv(file_path)
        print(f'Extracted {len(df)} rows from {filename}')
        return df

    def transform(self: , df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform data.
        
        Args:
            self (): 
            df (pd.DataFrame): 
        
        Returns:
            pd.DataFrame
        """
        # Remove duplicates
        df = df.drop_duplicates()

        # Fill missing values
        df = df.fillna(0)

        # Convert date columns
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])

        print(f'Transformed data: {len(df)} rows')
        return df

    def load(self: , df: pd.DataFrame, filename: str) -> None:
        """
        Load data to output.
        
        Args:
            self (): 
            df (pd.DataFrame): 
            filename (str): 
        
        Returns:
            None
        """
        output_path = self.output_dir / filename
        df.to_csv(output_path, index=False)
        print(f'Loaded {len(df)} rows to {filename}')

    def run(self: , filename: str) -> None:
        """
        Run complete ETL pipeline.
        
        Args:
            self (): 
            filename (str): 
        
        Returns:
            None
        """
        print(f'Starting pipeline for {filename}...')
        df = self.extract(filename)
        df = self.transform(df)
        self.load(df, f'processed_{filename}')
        print('Pipeline completed!')



if __name__ == '__main__':

    # Initialize pipeline
    pipeline = DataPipeline(
        input_dir=Path('data/raw'),
        output_dir=Path('data/processed')
    )

    # Process multiple files
    files = ['sales.csv', 'customers.csv', 'products.csv']
    for file in files:
        pipeline.run(file)

    print('All pipelines completed successfully!')