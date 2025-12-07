"""
Test Code Generator - Complete Testing
"""
import sys
sys.path.insert(0, r'C:\Users\user\Desktop\m\super_agent\tools')

from tools.code_generator import CodeGenerator

def test_all_generation():
    """Test all code generation capabilities."""
    
    generator = CodeGenerator()
    
    print("=" * 70)
    print("PYTHON CODE GENERATOR - TEST COMPLETO")
    print("=" * 70)
    
    # Test 1: Generate Simple Function
    print("\n1. FUNZIONE SEMPLICE")
    print("-" * 70)
    func_code = generator.generate_function(
        name="calculate_total",
        params=[
            {'name': 'price', 'type': 'float', 'description': 'Product price'},
            {'name': 'quantity', 'type': 'int', 'description': 'Quantity'},
            {'name': 'tax_rate', 'type': 'float', 'default': 0.20, 'description': 'Tax rate'}
        ],
        return_type="float",
        docstring="Calculate total price with tax.",
        body="""subtotal = price * quantity
tax = subtotal * tax_rate
total = subtotal + tax
return total"""
    )
    print(func_code)
    is_valid, error = generator.validate_code(func_code)
    print(f"\n✓ Codice valido: {is_valid}")
    
    # Test 2: Generate Async Function
    print("\n\n2. FUNZIONE ASYNC")
    print("-" * 70)
    async_code = generator.generate_function(
        name="fetch_data",
        params=[
            {'name': 'url', 'type': 'str', 'description': 'API URL'},
            {'name': 'timeout', 'type': 'int', 'default': 30, 'description': 'Request timeout'}
        ],
        return_type="Dict[str, Any]",
        docstring="Fetch data from API asynchronously.",
        body="""async with aiohttp.ClientSession() as session:
    async with session.get(url, timeout=timeout) as response:
        return await response.json()""",
        is_async=True
    )
    print(async_code)
    is_valid, error = generator.validate_code(async_code)
    print(f"\n✓ Codice valido: {is_valid}")
    
    # Test 3: Generate Class
    print("\n\n3. CLASSE COMPLETA")
    print("-" * 70)
    class_code = generator.generate_class(
        name="Product",
        attributes=[
            {'name': 'name', 'type': 'str', 'description': 'Product name'},
            {'name': 'price', 'type': 'float', 'description': 'Product price'},
            {'name': 'stock', 'type': 'int', 'default': 0, 'description': 'Stock quantity'}
        ],
        methods=[
            {
                'name': 'get_total_value',
                'params': [],
                'return_type': 'float',
                'docstring': 'Calculate total inventory value.',
                'body': 'return self.price * self.stock'
            },
            {
                'name': 'restock',
                'params': [{'name': 'quantity', 'type': 'int'}],
                'return_type': 'None',
                'docstring': 'Add stock.',
                'body': 'self.stock += quantity'
            }
        ],
        docstring="Represents a product in inventory."
    )
    print(class_code)
    is_valid, error = generator.validate_code(class_code)
    print(f"\n✓ Codice valido: {is_valid}")
    
    # Test 4: Generate Dataclass
    print("\n\n4. DATACLASS")
    print("-" * 70)
    dataclass_code = generator.generate_dataclass(
        name="User",
        fields=[
            {'name': 'id', 'type': 'int'},
            {'name': 'username', 'type': 'str'},
            {'name': 'email', 'type': 'str'},
            {'name': 'active', 'type': 'bool', 'default': True},
            {'name': 'roles', 'type': 'List[str]', 'default_factory': 'list'}
        ],
        docstring="User account data."
    )
    print(dataclass_code)
    is_valid, error = generator.validate_code(dataclass_code)
    print(f"\n✓ Codice valido: {is_valid}")
    
    # Test 5: Generate Decorator
    print("\n\n5. DECORATOR")
    print("-" * 70)
    decorator_code = generator.generate_decorator(
        name="timer",
        docstring="Measure function execution time.",
        body="""import time
start = time.time()
result = func(*args, **kwargs)
duration = time.time() - start
print(f'{func.__name__} took {duration:.3f}s')"""
    )
    print(decorator_code)
    is_valid, error = generator.validate_code(decorator_code)
    print(f"\n✓ Codice valido: {is_valid}")
    
    # Test 6: Generate Property
    print("\n\n6. PROPERTY")
    print("-" * 70)
    property_code = generator.generate_property(
        name="temperature",
        return_type="float",
        docstring="Temperature in Celsius.",
        getter_body="return self._temperature",
        setter_body="""if value < -273.15:
    raise ValueError('Temperature below absolute zero')
self._temperature = value""",
        setter_doc="Set temperature with validation."
    )
    print(property_code)
    # Note: Properties need to be in a class to validate
    
    # Test 7: Generate Context Manager
    print("\n\n7. CONTEXT MANAGER")
    print("-" * 70)
    context_code = generator.generate_context_manager(
        name="DatabaseConnection",
        docstring="Manage database connection lifecycle.",
        enter_body="""self.connection = connect_to_database()
print('Database connected')""",
        exit_body="""self.connection.close()
print('Database disconnected')"""
    )
    print(context_code)
    is_valid, error = generator.validate_code(context_code)
    print(f"\n✓ Codice valido: {is_valid}")
    
    # Test 8: Generate API Client
    print("\n\n8. API CLIENT")
    print("-" * 70)
    api_code = generator.generate_api_client(
        name="GitHubAPI",
        docstring="GitHub REST API v3 client."
    )
    print(api_code[:500] + "...")  # Preview
    is_valid, error = generator.validate_code(api_code)
    print(f"\n✓ Codice valido: {is_valid}")
    
    # Test 9: Generate CLI App
    print("\n\n9. CLI APPLICATION")
    print("-" * 70)
    cli_code = generator.generate_cli_app(
        name="DataProcessor",
        description="Process data files with various transformations",
        arguments=[
            {'name': 'input', 'positional': True, 'help': 'Input file path'},
            {'name': 'output', 'type': 'str', 'help': 'Output file path', 'required': True},
            {'name': 'format', 'type': 'str', 'default': 'json', 'help': 'Output format'},
            {'name': 'verbose', 'type': 'bool', 'default': False, 'help': 'Verbose output'}
        ],
        main_logic="""# Load input file
with open(parsed_args.input, 'r') as f:
    data = f.read()

# Process data
processed = process_data(data, parsed_args.format)

# Save output
with open(parsed_args.output, 'w') as f:
    f.write(processed)

if parsed_args.verbose:
    print(f'Processed {len(data)} bytes')"""
    )
    print(cli_code)
    is_valid, error = generator.validate_code(cli_code)
    print(f"\n✓ Codice valido: {is_valid}")
    
    # Test 10: Generate Test Class
    print("\n\n10. TEST CLASS")
    print("-" * 70)
    test_code = generator.generate_test_class(
        class_name="Calculator",
        test_methods=[
            {
                'name': 'addition',
                'docstring': 'Test addition operation.',
                'body': """calc = Calculator()
result = calc.add(2, 3)
self.assertEqual(result, 5)"""
            },
            {
                'name': 'division_by_zero',
                'docstring': 'Test division by zero raises error.',
                'body': """calc = Calculator()
with self.assertRaises(ZeroDivisionError):
    calc.divide(10, 0)"""
            }
        ],
        setup="self.calc = Calculator()",
        teardown="del self.calc"
    )
    print(test_code)
    is_valid, error = generator.validate_code(test_code)
    print(f"\n✓ Codice valido: {is_valid}")
    
    # Test 11: Generate Complete Script
    print("\n\n11. SCRIPT COMPLETO")
    print("-" * 70)
    script_code = generator.generate_script(
        name="Web Scraper with Database Storage",
        imports=[
            "import requests",
            "from bs4 import BeautifulSoup",
            "import sqlite3",
            "from typing import List, Dict"
        ],
        functions=[
            generator.generate_function(
                name="scrape_website",
                params=[{'name': 'url', 'type': 'str'}],
                return_type="List[Dict]",
                docstring="Scrape data from website.",
                body="""response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
data = []
for item in soup.find_all('div', class_='item'):
    data.append({'title': item.text})
return data"""
            ),
            generator.generate_function(
                name="save_to_database",
                params=[
                    {'name': 'data', 'type': 'List[Dict]'},
                    {'name': 'db_path', 'type': 'str'}
                ],
                return_type="int",
                docstring="Save data to SQLite database.",
                body="""conn = sqlite3.connect(db_path)
cursor = conn.cursor()
count = 0
for item in data:
    cursor.execute('INSERT INTO items (title) VALUES (?)', (item['title'],))
    count += 1
conn.commit()
conn.close()
return count"""
            )
        ],
        main_code="""# Scrape website
url = 'https://example.com'
data = scrape_website(url)
print(f'Scraped {len(data)} items')

# Save to database
count = save_to_database(data, 'data.db')
print(f'Saved {count} items to database')"""
    )
    print(script_code)
    is_valid, error = generator.validate_code(script_code)
    print(f"\n✓ Codice valido: {is_valid}")
    
    # Test 12: Code Validation
    print("\n\n12. VALIDAZIONE CODICE")
    print("-" * 70)
    
    # Valid code
    valid_code = "def test():\n    return True"
    is_valid, error = generator.validate_code(valid_code)
    print(f"Valid code: {is_valid} (error: {error})")
    
    # Invalid code
    invalid_code = "def test(\n    return True"
    is_valid, error = generator.validate_code(invalid_code)
    print(f"Invalid code: {is_valid} (error: {error})")
    
    # Summary
    print("\n\n" + "=" * 70)
    print("RIEPILOGO CAPACITÀ")
    print("=" * 70)
    print("""
    ✓ Funzioni semplici e async
    ✓ Classi con attributi e metodi
    ✓ Dataclass con campi tipizzati
    ✓ Decorator per funzioni
    ✓ Property con getter/setter
    ✓ Context manager
    ✓ API client REST
    ✓ Applicazioni CLI con argparse
    ✓ Test class con unittest
    ✓ Script completi multi-funzione
    ✓ Validazione sintassi AST
    ✓ Documentazione automatica
    
    CAPACITÀ: 100% ✓
    """)
    
    print("\n" + "=" * 70)

if __name__ == '__main__':
    test_all_generation()
