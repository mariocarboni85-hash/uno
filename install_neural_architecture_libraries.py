"""
Installer per librerie avanzate di Neural Architecture Design & Construction
Categorie: NAS, AutoML, Meta-Learning, Neural ODE, Graph Neural Networks, etc.
"""

import subprocess
import sys

# Librerie per Neural Architecture Search & AutoML
neural_architecture_libraries = {
    "Neural Architecture Search (NAS)": [
        "nni",                    # Neural Network Intelligence - Microsoft NAS framework
        "optuna",                 # Hyperparameter optimization framework
        "ray[tune]",              # Distributed hyperparameter tuning
        "hyperopt",               # Distributed hyperparameter optimization
        "keras-tuner",            # Hyperparameter tuning for Keras
        "autokeras",              # AutoML for deep learning
        "auto-sklearn",           # Automated machine learning toolkit
    ],
    
    "Meta-Learning & Few-Shot": [
        "learn2learn",            # Meta-learning library
        "higher",                 # Higher-order optimization for PyTorch
        "torchmeta",              # Meta-learning datasets and utilities
    ],
    
    "Neural Architecture Components": [
        "timm",                   # PyTorch Image Models - 700+ architectures
        "transformers",           # Hugging Face transformers (già installato ma aggiorniamo)
        "efficientnet-pytorch",   # EfficientNet models
        "pretrainedmodels",       # Pretrained CNN models
        "segmentation-models-pytorch",  # Segmentation architectures
    ],
    
    "Graph Neural Networks": [
        "torch-geometric",        # PyTorch Geometric - GNN library
        "dgl",                    # Deep Graph Library
        "spektral",               # Graph Neural Networks with Keras
        "networkx",               # Network analysis (dependency for GNNs)
    ],
    
    "Neural ODE & Differential Equations": [
        "torchdiffeq",            # Neural ODEs in PyTorch
        "diffrax",                # Differential equation solvers
    ],
    
    "Architecture Visualization & Analysis": [
        "torchviz",               # Visualize PyTorch computational graphs
        "tensorboard",            # TensorBoard visualization
        "wandb",                  # Weights & Biases experiment tracking
        "netron",                 # Neural network visualizer
        "graphviz",               # Graph visualization
    ],
    
    "Pruning & Compression": [
        "torch-pruning",          # Neural network pruning
        "neural-compressor",      # Intel Neural Compressor
        "nncf",                   # Neural Network Compression Framework
    ],
    
    "Quantization & Optimization": [
        "onnx",                   # Open Neural Network Exchange
        "onnxruntime",            # ONNX Runtime
        "pytorch-lightning",      # PyTorch Lightning framework
        "catalyst",               # PyTorch framework for DL research
    ],
    
    "Evolutionary & Genetic Algorithms": [
        "deap",                   # Distributed Evolutionary Algorithms
        "neat-python",            # NeuroEvolution of Augmenting Topologies
        "geneticalgorithm",       # Genetic Algorithm optimizer
    ],
    
    "Reinforcement Learning Architecture": [
        "stable-baselines3",      # RL algorithms implementations
        "tianshou",               # High-quality RL library
        "rlkit",                  # RL framework
        "pfrl",                   # PyTorch-based RL library
    ],
    
    "Neural Architecture Generation": [
        "torch-mlir",             # MLIR integration for PyTorch
        "fairscale",              # PyTorch extensions for large-scale training
        "accelerate",             # Hugging Face training acceleration
    ],
    
    "Model Analysis & Profiling": [
        "torchinfo",              # Model summary and analysis
        "thop",                   # PyTorch FLOPs counter
        "ptflops",                # PyTorch FLOPs estimation
        "fvcore",                 # Facebook core library (FLOPs, params)
    ],
    
    "Attention & Transformer Components": [
        "x-transformers",         # Experimental transformer architectures
        "performer-pytorch",      # Performer attention mechanism
        "linformer",              # Linear complexity transformers
        "reformer-pytorch",       # Reformer architecture
    ],
    
    "Neural Architecture DSL & IR": [
        "onnx-graphsurgeon",      # ONNX graph manipulation
        "tensorrt",               # NVIDIA TensorRT (se disponibile)
    ]
}

def install_libraries():
    """Installa tutte le librerie"""
    
    print("=" * 80)
    print("NEURAL ARCHITECTURE DESIGN & CONSTRUCTION LIBRARIES INSTALLER")
    print("=" * 80)
    
    total_libraries = sum(len(libs) for libs in neural_architecture_libraries.values())
    installed = 0
    failed = []
    
    print(f"\nTotal libraries to install: {total_libraries}")
    print(f"Categories: {len(neural_architecture_libraries)}\n")
    
    for category, libraries in neural_architecture_libraries.items():
        print(f"\n{'=' * 80}")
        print(f"CATEGORY: {category}")
        print(f"{'=' * 80}")
        print(f"Libraries: {len(libraries)}\n")
        
        for lib in libraries:
            try:
                print(f"[{installed + 1}/{total_libraries}] Installing {lib}...", end=" ")
                
                # Installa con pip
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", lib, "--quiet"],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if result.returncode == 0:
                    print("[OK]")
                    installed += 1
                else:
                    print("[FAILED]")
                    failed.append((lib, result.stderr))
                    
            except subprocess.TimeoutExpired:
                print("[TIMEOUT]")
                failed.append((lib, "Installation timeout"))
            except Exception as e:
                print(f"[ERROR: {str(e)}]")
                failed.append((lib, str(e)))
    
    # Summary
    print("\n" + "=" * 80)
    print("INSTALLATION SUMMARY")
    print("=" * 80)
    print(f"\nTotal libraries: {total_libraries}")
    print(f"Successfully installed: {installed}")
    print(f"Failed: {len(failed)}")
    print(f"Success rate: {(installed/total_libraries)*100:.1f}%")
    
    if failed:
        print(f"\n{'=' * 80}")
        print("FAILED INSTALLATIONS:")
        print('=' * 80)
        for lib, error in failed:
            print(f"\n  Library: {lib}")
            print(f"  Error: {error[:200]}")
    
    print("\n" + "=" * 80)
    print("[OK] Installation complete!")
    print("=" * 80)
    
    return installed, failed

if __name__ == "__main__":
    installed, failed = install_libraries()
    
    # Exit code
    sys.exit(0 if len(failed) == 0 else 1)
