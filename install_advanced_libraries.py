"""
Setup Advanced Libraries for Super Agent
Install programming, computer science, and advanced mathematics libraries
"""
import sys
sys.path.insert(0, 'tools')

from tools.venv_manager import VirtualEnvironmentManager

def install_advanced_libraries():
    """Install all advanced libraries."""
    
    manager = VirtualEnvironmentManager()
    
    print("=" * 80)
    print("SUPER AGENT - INSTALLAZIONE LIBRERIE AVANZATE")
    print("=" * 80)
    
    # Create advanced environment
    print("\n1. Creazione ambiente virtuale avanzato...")
    result = manager.create_venv(
        name="super_agent_advanced",
        prompt="(SA-Advanced)"
    )
    
    if result['success']:
        print(f"✓ Ambiente creato: {result['name']}")
        print(f"  Path: {result['path']}")
    else:
        print(f"✗ Errore: {result['error']}")
        return
    
    env_name = "super_agent_advanced"
    
    # Define library categories
    libraries = {
        "Matematica Avanzata": [
            "numpy",           # Arrays e algebra lineare
            "scipy",           # Computazione scientifica
            "sympy",           # Matematica simbolica
            "mpmath",          # Aritmetica precisione arbitraria
            "numba",           # JIT compilation per NumPy
            "numexpr",         # Espressioni numeriche veloci
        ],
        
        "Algebra e Geometria": [
            "networkx",        # Teoria dei grafi
            "pygraphviz",      # Visualizzazione grafi (richiede Graphviz)
            "matplotlib",      # Plotting
            "seaborn",         # Visualizzazione statistica
        ],
        
        "Data Science & ML": [
            "pandas",          # Data manipulation
            "scikit-learn",    # Machine Learning
            "statsmodels",     # Modelli statistici
            "xgboost",         # Gradient boosting
            "lightgbm",        # Light GBM
        ],
        
        "Deep Learning": [
            "torch",           # PyTorch
            "transformers",    # Hugging Face
            "tensorflow",      # TensorFlow
            "keras",           # Keras API
        ],
        
        "Computer Vision": [
            "opencv-python",   # OpenCV
            "pillow",          # Image processing
            "scikit-image",    # Image algorithms
        ],
        
        "Natural Language Processing": [
            "nltk",            # Natural Language Toolkit
            "spacy",           # Industrial NLP
            "gensim",          # Topic modeling
            "textblob",        # Simple NLP
        ],
        
        "Ottimizzazione": [
            "cvxpy",           # Convex optimization
            "pulp",            # Linear programming
            "ortools",         # Google OR-Tools
        ],
        
        "Algoritmi e Strutture Dati": [
            "sortedcontainers", # Sorted collections
            "bintrees",        # Binary trees
            "heapdict",        # Heap dict
        ],
        
        "Crittografia e Sicurezza": [
            "cryptography",    # Crittografia moderna
            "pycryptodome",    # Crypto primitives
            "hashlib",         # Hashing (built-in)
        ],
        
        "Compilatori e Parsing": [
            "ply",             # Lex/Yacc per Python
            "pyparsing",       # Parser generator
            "lark",            # Modern parsing
        ],
        
        "Parallel Computing": [
            "joblib",          # Parallel loops
            "dask",            # Parallel arrays
            "ray",             # Distributed computing
            "multiprocess",    # Better multiprocessing
        ],
        
        "Testing e Quality": [
            "pytest",          # Testing framework
            "hypothesis",      # Property-based testing
            "coverage",        # Code coverage
            "black",           # Code formatter
            "pylint",          # Linter
            "mypy",            # Static type checker
        ],
        
        "Database e Storage": [
            "sqlalchemy",      # SQL toolkit
            "redis",           # Redis client
            "pymongo",         # MongoDB
            "psycopg2-binary", # PostgreSQL
        ],
        
        "Web e API": [
            "fastapi",         # Modern API framework
            "uvicorn",         # ASGI server
            "httpx",           # Async HTTP
            "websockets",      # WebSocket protocol
        ],
        
        "DevOps e Automation": [
            "docker",          # Docker SDK
            "kubernetes",      # K8s client
            "ansible",         # Automation
            "fabric",          # SSH automation
        ],
        
        "Utilities Avanzate": [
            "rich",            # Rich text/formatting
            "typer",           # CLI framework
            "pydantic",        # Data validation
            "arrow",           # Better dates/times
            "loguru",          # Logging
            "tqdm",            # Progress bars
        ]
    }
    
    total_packages = sum(len(pkgs) for pkgs in libraries.values())
    installed = 0
    failed = []
    
    print(f"\n2. Installazione {total_packages} librerie avanzate...")
    print("=" * 80)
    
    for category, packages in libraries.items():
        print(f"\n📚 {category}")
        print("-" * 80)
        
        for package in packages:
            print(f"  Installando {package}...", end=" ", flush=True)
            
            result = manager.install_package(env_name, package)
            
            if result['success']:
                print("✓")
                installed += 1
            else:
                print(f"✗ ({result.get('error', 'Unknown error')})")
                failed.append(package)
    
    # Summary
    print("\n" + "=" * 80)
    print("RIEPILOGO INSTALLAZIONE")
    print("=" * 80)
    print(f"Totale librerie: {total_packages}")
    print(f"Installate: {installed}")
    print(f"Fallite: {len(failed)}")
    
    if failed:
        print(f"\nLibrerie non installate:")
        for pkg in failed:
            print(f"  - {pkg}")
    
    # Export requirements
    print("\n3. Export requirements...")
    result = manager.export_requirements(
        env_name,
        "requirements_advanced.txt"
    )
    
    if result['success']:
        print(f"✓ Requirements esportati: {result['output_file']}")
        print(f"  Packages: {result['packages_count']}")
    
    # Get environment info
    print("\n4. Informazioni ambiente...")
    info = manager.get_venv_info(env_name)
    
    print(f"Nome: {info['name']}")
    print(f"Python: {info['python_version']}")
    print(f"Pip: {info['pip_version']}")
    print(f"Packages installati: {info['packages_count']}")
    
    # Activation command
    print("\n5. Attivazione ambiente...")
    cmd_info = manager.get_activation_command(env_name)
    print(f"Comando: {cmd_info['command']}")
    
    # Final summary
    print("\n" + "=" * 80)
    print("CAPACITÀ INSTALLATE")
    print("=" * 80)
    print("""
    ✓ Matematica Avanzata (NumPy, SciPy, SymPy)
    ✓ Algebra Lineare & Geometria
    ✓ Machine Learning (scikit-learn, XGBoost)
    ✓ Deep Learning (PyTorch, TensorFlow)
    ✓ Computer Vision (OpenCV, PIL)
    ✓ Natural Language Processing (NLTK, spaCy)
    ✓ Ottimizzazione (CVXPY, OR-Tools)
    ✓ Algoritmi & Strutture Dati
    ✓ Crittografia & Sicurezza
    ✓ Compilatori & Parsing
    ✓ Parallel Computing (Dask, Ray)
    ✓ Testing & Quality (pytest, mypy)
    ✓ Database (SQLAlchemy, MongoDB)
    ✓ Web & API (FastAPI, WebSockets)
    ✓ DevOps (Docker, Kubernetes)
    ✓ Utilities Avanzate (Rich, Pydantic)
    
    Super Agent ora ha accesso a librerie avanzate di:
    • Programmazione
    • Ingegneria informatica
    • Matematica avanzata
    • Machine Learning & AI
    • Computer Science
    """)
    
    print("\n" + "=" * 80)
    print("✓ INSTALLAZIONE COMPLETATA")
    print("=" * 80)

if __name__ == '__main__':
    install_advanced_libraries()
