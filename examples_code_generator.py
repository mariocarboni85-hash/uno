"""
Practical Examples - Code Generator Usage
"""
import sys
sys.path.insert(0, r'C:\Users\user\Desktop\m\super_agent\tools')

from tools.code_generator import CodeGenerator

def example_1_web_api_service():
    """Generate a complete REST API service."""
    print("=" * 70)
    print("ESEMPIO 1: WEB API SERVICE COMPLETO")
    print("=" * 70)
    
    gen = CodeGenerator()
    
    # Generate the complete API service
    api_service = gen.generate_script(
        name="User Management API Service",
        imports=[
            "from flask import Flask, request, jsonify",
            "from typing import Dict, List, Optional",
            "import sqlite3",
            "from datetime import datetime"
        ],
        functions=[
            gen.generate_class(
                name="UserDatabase",
                attributes=[
                    {'name': 'db_path', 'type': 'str', 'description': 'Database file path'}
                ],
                methods=[
                    {
                        'name': 'create_user',
                        'params': [
                            {'name': 'username', 'type': 'str'},
                            {'name': 'email', 'type': 'str'}
                        ],
                        'return_type': 'int',
                        'docstring': 'Create new user.',
                        'body': """conn = sqlite3.connect(self.db_path)
cursor = conn.cursor()
cursor.execute(
    'INSERT INTO users (username, email, created_at) VALUES (?, ?, ?)',
    (username, email, datetime.now().isoformat())
)
user_id = cursor.lastrowid
conn.commit()
conn.close()
return user_id"""
                    },
                    {
                        'name': 'get_user',
                        'params': [{'name': 'user_id', 'type': 'int'}],
                        'return_type': 'Optional[Dict]',
                        'docstring': 'Get user by ID.',
                        'body': """conn = sqlite3.connect(self.db_path)
cursor = conn.cursor()
cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
row = cursor.fetchone()
conn.close()
if row:
    return {'id': row[0], 'username': row[1], 'email': row[2]}
return None"""
                    }
                ],
                docstring="Database operations for user management."
            )
        ],
        main_code="""# Initialize Flask app
app = Flask(__name__)
db = UserDatabase('users.db')

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user_id = db.create_user(data['username'], data['email'])
    return jsonify({'id': user_id, 'status': 'created'}), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.get_user(user_id)
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

# Run server
app.run(host='0.0.0.0', port=5000, debug=True)"""
    )
    
    print(api_service)
    print("\n✓ API Service generato con successo!")
    
    # Save to file
    with open('generated_api_service.py', 'w') as f:
        f.write(api_service)
    print("✓ Salvato in: generated_api_service.py")


def example_2_data_processing_pipeline():
    """Generate a data processing pipeline."""
    print("\n\n" + "=" * 70)
    print("ESEMPIO 2: DATA PROCESSING PIPELINE")
    print("=" * 70)
    
    gen = CodeGenerator()
    
    pipeline = gen.generate_script(
        name="ETL Data Pipeline",
        imports=[
            "import pandas as pd",
            "import json",
            "from typing import Dict, List",
            "from pathlib import Path"
        ],
        functions=[
            gen.generate_class(
                name="DataPipeline",
                attributes=[
                    {'name': 'input_dir', 'type': 'Path', 'description': 'Input directory'},
                    {'name': 'output_dir', 'type': 'Path', 'description': 'Output directory'}
                ],
                methods=[
                    {
                        'name': 'extract',
                        'params': [{'name': 'filename', 'type': 'str'}],
                        'return_type': 'pd.DataFrame',
                        'docstring': 'Extract data from CSV.',
                        'body': """file_path = self.input_dir / filename
df = pd.read_csv(file_path)
print(f'Extracted {len(df)} rows from {filename}')
return df"""
                    },
                    {
                        'name': 'transform',
                        'params': [{'name': 'df', 'type': 'pd.DataFrame'}],
                        'return_type': 'pd.DataFrame',
                        'docstring': 'Transform data.',
                        'body': """# Remove duplicates
df = df.drop_duplicates()

# Fill missing values
df = df.fillna(0)

# Convert date columns
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'])

print(f'Transformed data: {len(df)} rows')
return df"""
                    },
                    {
                        'name': 'load',
                        'params': [
                            {'name': 'df', 'type': 'pd.DataFrame'},
                            {'name': 'filename', 'type': 'str'}
                        ],
                        'return_type': 'None',
                        'docstring': 'Load data to output.',
                        'body': """output_path = self.output_dir / filename
df.to_csv(output_path, index=False)
print(f'Loaded {len(df)} rows to {filename}')"""
                    },
                    {
                        'name': 'run',
                        'params': [{'name': 'filename', 'type': 'str'}],
                        'return_type': 'None',
                        'docstring': 'Run complete ETL pipeline.',
                        'body': """print(f'Starting pipeline for {filename}...')
df = self.extract(filename)
df = self.transform(df)
self.load(df, f'processed_{filename}')
print('Pipeline completed!')"""
                    }
                ],
                docstring="ETL pipeline for data processing."
            )
        ],
        main_code="""# Initialize pipeline
pipeline = DataPipeline(
    input_dir=Path('data/raw'),
    output_dir=Path('data/processed')
)

# Process multiple files
files = ['sales.csv', 'customers.csv', 'products.csv']
for file in files:
    pipeline.run(file)

print('All pipelines completed successfully!')"""
    )
    
    print(pipeline)
    print("\n✓ Data Pipeline generato con successo!")
    
    with open('generated_data_pipeline.py', 'w') as f:
        f.write(pipeline)
    print("✓ Salvato in: generated_data_pipeline.py")


def example_3_async_web_scraper():
    """Generate async web scraper."""
    print("\n\n" + "=" * 70)
    print("ESEMPIO 3: ASYNC WEB SCRAPER")
    print("=" * 70)
    
    gen = CodeGenerator()
    
    scraper = gen.generate_script(
        name="Asynchronous Web Scraper",
        imports=[
            "import asyncio",
            "import aiohttp",
            "from bs4 import BeautifulSoup",
            "from typing import List, Dict",
            "import json"
        ],
        functions=[
            gen.generate_function(
                name="fetch_page",
                params=[
                    {'name': 'session', 'type': 'aiohttp.ClientSession'},
                    {'name': 'url', 'type': 'str'}
                ],
                return_type="str",
                docstring="Fetch page content.",
                body="""async with session.get(url) as response:
    return await response.text()""",
                is_async=True
            ),
            gen.generate_function(
                name="parse_page",
                params=[
                    {'name': 'html', 'type': 'str'},
                    {'name': 'url', 'type': 'str'}
                ],
                return_type="Dict",
                docstring="Parse HTML and extract data.",
                body="""soup = BeautifulSoup(html, 'html.parser')

# Extract title
title = soup.find('title')
title_text = title.text if title else 'No title'

# Extract links
links = [a.get('href') for a in soup.find_all('a', href=True)]

# Extract headings
headings = [h.text for h in soup.find_all(['h1', 'h2', 'h3'])]

return {
    'url': url,
    'title': title_text,
    'links_count': len(links),
    'links': links[:10],  # First 10 links
    'headings': headings
}"""
            ),
            gen.generate_function(
                name="scrape_urls",
                params=[
                    {'name': 'urls', 'type': 'List[str]'}
                ],
                return_type="List[Dict]",
                docstring="Scrape multiple URLs concurrently.",
                body="""async with aiohttp.ClientSession() as session:
    tasks = []
    for url in urls:
        task = fetch_page(session, url)
        tasks.append(task)
    
    # Fetch all pages concurrently
    pages = await asyncio.gather(*tasks)
    
    # Parse all pages
    results = []
    for url, html in zip(urls, pages):
        data = parse_page(html, url)
        results.append(data)
    
    return results""",
                is_async=True
            )
        ],
        main_code="""# URLs to scrape
urls = [
    'https://example.com',
    'https://python.org',
    'https://github.com'
]

# Run async scraper
results = asyncio.run(scrape_urls(urls))

# Save results
with open('scraped_data.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f'Scraped {len(results)} pages')
for result in results:
    print(f"- {result['title']}: {result['links_count']} links")"""
    )
    
    print(scraper)
    print("\n✓ Async Scraper generato con successo!")
    
    with open('generated_async_scraper.py', 'w') as f:
        f.write(scraper)
    print("✓ Salvato in: generated_async_scraper.py")


def example_4_machine_learning_trainer():
    """Generate ML model trainer."""
    print("\n\n" + "=" * 70)
    print("ESEMPIO 4: MACHINE LEARNING TRAINER")
    print("=" * 70)
    
    gen = CodeGenerator()
    
    ml_trainer = gen.generate_script(
        name="Machine Learning Model Trainer",
        imports=[
            "import pandas as pd",
            "import numpy as np",
            "from sklearn.model_selection import train_test_split",
            "from sklearn.ensemble import RandomForestClassifier",
            "from sklearn.metrics import accuracy_score, classification_report",
            "import joblib",
            "from typing import Tuple"
        ],
        functions=[
            gen.generate_class(
                name="ModelTrainer",
                attributes=[
                    {'name': 'model', 'type': 'RandomForestClassifier', 'description': 'ML model'},
                    {'name': 'feature_names', 'type': 'list', 'default': '[]', 'description': 'Feature names'}
                ],
                methods=[
                    {
                        'name': 'load_data',
                        'params': [{'name': 'csv_path', 'type': 'str'}],
                        'return_type': 'Tuple[pd.DataFrame, pd.Series]',
                        'docstring': 'Load and prepare data.',
                        'body': """df = pd.read_csv(csv_path)
print(f'Loaded {len(df)} samples')

# Separate features and target
X = df.drop('target', axis=1)
y = df['target']

self.feature_names = X.columns.tolist()

return X, y"""
                    },
                    {
                        'name': 'train',
                        'params': [
                            {'name': 'X', 'type': 'pd.DataFrame'},
                            {'name': 'y', 'type': 'pd.Series'},
                            {'name': 'test_size', 'type': 'float', 'default': 0.2}
                        ],
                        'return_type': 'Dict',
                        'docstring': 'Train the model.',
                        'body': """# Split data
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
}"""
                    },
                    {
                        'name': 'predict',
                        'params': [{'name': 'X', 'type': 'pd.DataFrame'}],
                        'return_type': 'np.ndarray',
                        'docstring': 'Make predictions.',
                        'body': """return self.model.predict(X)"""
                    },
                    {
                        'name': 'save',
                        'params': [{'name': 'path', 'type': 'str'}],
                        'return_type': 'None',
                        'docstring': 'Save model to disk.',
                        'body': """joblib.dump(self.model, path)
print(f'Model saved to {path}')"""
                    }
                ],
                docstring="Train and manage ML models."
            )
        ],
        main_code="""# Initialize trainer
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
trainer.save('model.pkl')"""
    )
    
    print(ml_trainer)
    print("\n✓ ML Trainer generato con successo!")
    
    with open('generated_ml_trainer.py', 'w') as f:
        f.write(ml_trainer)
    print("✓ Salvato in: generated_ml_trainer.py")


if __name__ == '__main__':
    print("\n" + "🚀 " * 35)
    print("ESEMPI PRATICI - GENERAZIONE CODICE PYTHON")
    print("🚀 " * 35)
    
    example_1_web_api_service()
    example_2_data_processing_pipeline()
    example_3_async_web_scraper()
    example_4_machine_learning_trainer()
    
    print("\n\n" + "=" * 70)
    print("TUTTI GLI ESEMPI GENERATI CON SUCCESSO!")
    print("=" * 70)
    print("""
    File generati:
    1. generated_api_service.py       - REST API con Flask
    2. generated_data_pipeline.py     - ETL Pipeline con Pandas
    3. generated_async_scraper.py     - Web Scraper Async
    4. generated_ml_trainer.py        - ML Trainer con Sklearn
    
    Ogni file è completo e pronto all'uso!
    """)
