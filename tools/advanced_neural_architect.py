"""
Advanced Neural Architecture Designer - Sistema esperto con NAS, AutoML, GNN
Estensione del Neural Agent Builder con capacità avanzate
"""

try:
    import torch
    import torch.nn as nn
    from typing import Dict, List, Any, Optional, Tuple
    from pathlib import Path
    import json
    # NAS & AutoML
    import optuna
    import nni
    from hyperopt import hp, fmin, tpe, Trials
    # Architecture Components
    import timm
    from efficientnet_pytorch import EfficientNet
    # Graph Neural Networks
    import torch_geometric
    from torch_geometric.nn import GCNConv, GATConv, SAGEConv
    try:
        import dgl
        DGL_AVAILABLE = True
    except:
        DGL_AVAILABLE = False
    import networkx as nx
    # Neural ODE
    from torchdiffeq import odeint
    # Visualization & Analysis
    import torchviz
    from torchinfo import summary
    from thop import profile
    import wandb
    ADVANCED_NEURAL_LIBS_AVAILABLE = True
except ImportError:
    ADVANCED_NEURAL_LIBS_AVAILABLE = False

# Pruning & Compression
import torch_pruning as tp
import nncf

# Evolutionary
from deap import base, creator, tools, algorithms
import neat

# Optimization
import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping

# Transformers
from x_transformers import Encoder, Decoder
from performer_pytorch import Performer

# Pretrained Models
import pretrainedmodels


class AdvancedNeuralArchitect:
    """Architetto neurale avanzato con NAS, AutoML, GNN capabilities"""
    
    def __init__(self, workspace_path: str = "."):
        self.workspace = Path(workspace_path)
        self.architectures_dir = self.workspace / "advanced_architectures"
        self.architectures_dir.mkdir(exist_ok=True)
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Architecture registry
        self.pretrained_registry = self._load_pretrained_registry()
        
    def _load_pretrained_registry(self) -> Dict[str, Any]:
        """Carica registry di architetture pretrained"""
        return {
            'timm_models': timm.list_models(),  # 700+ models
            'efficientnet': ['efficientnet-b0', 'efficientnet-b1', 'efficientnet-b2',
                            'efficientnet-b3', 'efficientnet-b4', 'efficientnet-b5',
                            'efficientnet-b6', 'efficientnet-b7'],
            'pretrained_models': pretrainedmodels.model_names
        }
    
    def create_graph_neural_network(self, 
                                    gnn_type: str = 'gcn',
                                    input_dim: int = 128,
                                    hidden_dims: List[int] = None,
                                    output_dim: int = 64,
                                    num_layers: int = 3,
                                    activation: str = 'relu',
                                    dropout: float = 0.5) -> nn.Module:
        """Crea Graph Neural Network"""
        
        if hidden_dims is None:
            hidden_dims = [256, 128]
        
        print(f"\n[*] Creating Graph Neural Network")
        print(f"   Type: {gnn_type.upper()}")
        print(f"   Layers: {num_layers}")
        print(f"   Hidden dims: {hidden_dims}")
        
        class GNNModel(nn.Module):
            def __init__(self):
                super().__init__()
                self.layers = nn.ModuleList()
                
                # Input layer
                prev_dim = input_dim
                for hidden_dim in hidden_dims:
                    if gnn_type == 'gcn':
                        self.layers.append(GCNConv(prev_dim, hidden_dim))
                    elif gnn_type == 'gat':
                        self.layers.append(GATConv(prev_dim, hidden_dim, heads=4))
                    elif gnn_type == 'sage':
                        self.layers.append(SAGEConv(prev_dim, hidden_dim))
                    prev_dim = hidden_dim
                
                # Output layer
                if gnn_type == 'gcn':
                    self.layers.append(GCNConv(prev_dim, output_dim))
                elif gnn_type == 'gat':
                    self.layers.append(GATConv(prev_dim, output_dim, heads=1))
                elif gnn_type == 'sage':
                    self.layers.append(SAGEConv(prev_dim, output_dim))
                
                self.dropout = nn.Dropout(dropout)
                self.activation = nn.ReLU() if activation == 'relu' else nn.Tanh()
            
            def forward(self, x, edge_index):
                for i, layer in enumerate(self.layers[:-1]):
                    x = layer(x, edge_index)
                    x = self.activation(x)
                    x = self.dropout(x)
                
                x = self.layers[-1](x, edge_index)
                return x
        
        model = GNNModel().to(self.device)
        
        print(f"[OK] GNN model created")
        return model
    
    def create_neural_ode(self,
                         input_dim: int = 128,
                         hidden_dim: int = 256,
                         output_dim: int = 64,
                         ode_layers: int = 3) -> nn.Module:
        """Crea Neural ODE model"""
        
        print(f"\n[*] Creating Neural ODE")
        print(f"   Input dim: {input_dim}")
        print(f"   Hidden dim: {hidden_dim}")
        print(f"   ODE layers: {ode_layers}")
        
        class ODEFunc(nn.Module):
            def __init__(self, dim):
                super().__init__()
                self.net = nn.Sequential(
                    nn.Linear(dim, hidden_dim),
                    nn.ReLU(),
                    nn.Linear(hidden_dim, hidden_dim),
                    nn.ReLU(),
                    nn.Linear(hidden_dim, dim)
                )
            
            def forward(self, t, x):
                return self.net(x)
        
        class NeuralODE(nn.Module):
            def __init__(self, device):
                super().__init__()
                self.encoder = nn.Linear(input_dim, hidden_dim)
                self.ode_func = ODEFunc(hidden_dim)
                self.decoder = nn.Linear(hidden_dim, output_dim)
                self.t = torch.tensor([0., 1.]).to(device)
            
            def forward(self, x):
                # Encode
                x = self.encoder(x)
                
                # Solve ODE
                x = odeint(self.ode_func, x, self.t)[1]
                
                # Decode
                x = self.decoder(x)
                return x
        
        model = NeuralODE(self.device).to(self.device)
        
        print(f"[OK] Neural ODE created")
        return model
    
    def create_transformer_architecture(self,
                                       arch_type: str = 'encoder',
                                       vocab_size: int = 50000,
                                       max_seq_len: int = 512,
                                       dim: int = 512,
                                       depth: int = 6,
                                       heads: int = 8,
                                       use_performer: bool = False) -> nn.Module:
        """Crea architettura Transformer avanzata"""
        
        print(f"\n[*] Creating Transformer Architecture")
        print(f"   Type: {arch_type}")
        print(f"   Performer: {use_performer}")
        print(f"   Layers: {depth}")
        print(f"   Heads: {heads}")
        
        if use_performer:
            # Performer - Linear attention
            model = Performer(
                dim=dim,
                depth=depth,
                heads=heads,
                dim_head=dim // heads,
                causal=False
            ).to(self.device)
        else:
            # Standard Transformer
            if arch_type == 'encoder':
                model = Encoder(
                    dim=dim,
                    depth=depth,
                    heads=heads,
                    attn_dim_head=dim // heads
                ).to(self.device)
            else:
                model = Decoder(
                    dim=dim,
                    depth=depth,
                    heads=heads,
                    attn_dim_head=dim // heads
                ).to(self.device)
        
        print(f"[OK] Transformer created")
        return model
    
    def load_pretrained_backbone(self, 
                                model_name: str = 'resnet50',
                                num_classes: int = 1000) -> nn.Module:
        """Carica backbone pretrained da timm o pretrainedmodels"""
        
        print(f"\n[*] Loading pretrained backbone: {model_name}")
        
        try:
            # Try timm first (700+ models)
            if model_name in self.pretrained_registry['timm_models']:
                model = timm.create_model(model_name, pretrained=True, num_classes=num_classes)
                print(f"[OK] Loaded from timm")
            else:
                # Try pretrainedmodels
                model = pretrainedmodels.__dict__[model_name](pretrained='imagenet')
                print(f"[OK] Loaded from pretrainedmodels")
            
            return model.to(self.device)
            
        except Exception as e:
            print(f"[ERROR] Failed to load {model_name}: {e}")
            return None
    
    def optimize_with_optuna(self,
                            objective_fn,
                            n_trials: int = 100,
                            study_name: str = "neural_arch_optimization") -> Dict[str, Any]:
        """Ottimizza architettura con Optuna"""
        
        print(f"\n[*] Starting Optuna Optimization")
        print(f"   Trials: {n_trials}")
        print(f"   Study: {study_name}")
        
        study = optuna.create_study(
            study_name=study_name,
            direction='maximize',
            sampler=optuna.samplers.TPESampler()
        )
        
        study.optimize(objective_fn, n_trials=n_trials, show_progress_bar=True)
        
        best_params = study.best_params
        best_value = study.best_value
        
        print(f"\n[OK] Optimization complete")
        print(f"   Best value: {best_value:.4f}")
        print(f"   Best params: {best_params}")
        
        return {
            'best_params': best_params,
            'best_value': best_value,
            'study': study
        }
    
    def evolve_architecture_with_neat(self,
                                     config_path: str,
                                     fitness_fn,
                                     generations: int = 100) -> Any:
        """Evolve neural architecture con NEAT"""
        
        print(f"\n[*] Starting NEAT Evolution")
        print(f"   Generations: {generations}")
        
        # NEAT configuration
        config = neat.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_path
        )
        
        # Create population
        population = neat.Population(config)
        
        # Add reporters
        population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        population.add_reporter(stats)
        
        # Run evolution
        winner = population.run(fitness_fn, generations)
        
        print(f"[OK] Evolution complete")
        return winner
    
    def analyze_architecture(self, 
                           model: nn.Module,
                           input_size: Tuple[int, ...] = (1, 3, 224, 224)) -> Dict[str, Any]:
        """Analizza architettura completa"""
        
        print(f"\n[*] Analyzing Architecture")
        
        # Model summary
        model_stats = summary(model, input_size=input_size, verbose=0)
        
        # FLOPs & Parameters
        dummy_input = torch.randn(*input_size).to(self.device)
        flops, params = profile(model, inputs=(dummy_input,), verbose=False)
        
        analysis = {
            'total_params': model_stats.total_params,
            'trainable_params': model_stats.trainable_params,
            'total_flops': flops,
            'model_size_mb': model_stats.total_params * 4 / (1024 ** 2),  # float32
            'input_size': input_size,
            'layers': len(list(model.modules())),
        }
        
        print(f"   Parameters: {analysis['total_params']:,}")
        print(f"   FLOPs: {analysis['total_flops']:,}")
        print(f"   Model size: {analysis['model_size_mb']:.2f} MB")
        
        return analysis
    
    def visualize_architecture(self,
                              model: nn.Module,
                              input_size: Tuple[int, ...] = (1, 3, 224, 224),
                              save_path: str = None) -> str:
        """Visualizza architettura con torchviz"""
        
        print(f"\n[*] Visualizing Architecture")
        
        dummy_input = torch.randn(*input_size).to(self.device)
        output = model(dummy_input)
        
        # Create computation graph
        graph = torchviz.make_dot(output, params=dict(model.named_parameters()))
        
        if save_path is None:
            save_path = str(self.architectures_dir / "architecture_graph")
        
        graph.render(save_path, format='pdf')
        
        print(f"[OK] Graph saved to {save_path}.pdf")
        return f"{save_path}.pdf"
    
    def prune_model(self,
                   model: nn.Module,
                   example_input: torch.Tensor,
                   pruning_ratio: float = 0.5) -> nn.Module:
        """Prune model per ridurre parametri"""
        
        print(f"\n[*] Pruning Model")
        print(f"   Pruning ratio: {pruning_ratio}")
        
        # Original stats
        original_params = sum(p.numel() for p in model.parameters())
        
        # Importance-based pruning
        imp = tp.importance.MagnitudeImportance(p=2)
        
        ignored_layers = []
        for m in model.modules():
            if isinstance(m, (nn.Linear, nn.Conv2d)):
                pass  # Prune these layers
            else:
                ignored_layers.append(m)
        
        pruner = tp.pruner.MagnitudePruner(
            model,
            example_input,
            importance=imp,
            pruning_ratio=pruning_ratio,
            ignored_layers=ignored_layers
        )
        
        pruned_model = pruner.prune()
        
        # New stats
        pruned_params = sum(p.numel() for p in pruned_model.parameters())
        reduction = (1 - pruned_params / original_params) * 100
        
        print(f"[OK] Model pruned")
        print(f"   Original params: {original_params:,}")
        print(f"   Pruned params: {pruned_params:,}")
        print(f"   Reduction: {reduction:.1f}%")
        
        return pruned_model
    
    def create_lightning_module(self,
                               model: nn.Module,
                               learning_rate: float = 0.001) -> pl.LightningModule:
        """Wrap model in PyTorch Lightning module"""
        
        class LitModel(pl.LightningModule):
            def __init__(self, model, lr):
                super().__init__()
                self.model = model
                self.lr = lr
                self.criterion = nn.CrossEntropyLoss()
            
            def forward(self, x):
                return self.model(x)
            
            def training_step(self, batch, batch_idx):
                x, y = batch
                y_hat = self(x)
                loss = self.criterion(y_hat, y)
                self.log('train_loss', loss)
                return loss
            
            def validation_step(self, batch, batch_idx):
                x, y = batch
                y_hat = self(x)
                loss = self.criterion(y_hat, y)
                self.log('val_loss', loss)
                return loss
            
            def configure_optimizers(self):
                return torch.optim.Adam(self.parameters(), lr=self.lr)
        
        return LitModel(model, learning_rate)
    
    def export_to_onnx(self,
                      model: nn.Module,
                      input_size: Tuple[int, ...],
                      export_path: str = None) -> str:
        """Export model to ONNX format"""
        
        if export_path is None:
            export_path = str(self.architectures_dir / "model.onnx")
        
        print(f"\n[*] Exporting to ONNX")
        
        dummy_input = torch.randn(*input_size).to(self.device)
        
        torch.onnx.export(
            model,
            dummy_input,
            export_path,
            export_params=True,
            opset_version=14,
            do_constant_folding=True,
            input_names=['input'],
            output_names=['output'],
            dynamic_axes={
                'input': {0: 'batch_size'},
                'output': {0: 'batch_size'}
            }
        )
        
        print(f"[OK] Model exported to {export_path}")
        return export_path
    
    def get_architecture_recommendations(self, 
                                        task_type: str,
                                        dataset_size: str = 'medium',
                                        compute_budget: str = 'medium') -> List[str]:
        """Raccomanda architetture basate su task e constraints"""
        
        recommendations = []
        
        if task_type == 'image_classification':
            if compute_budget == 'low':
                recommendations = ['mobilenet_v3_small', 'efficientnet_b0', 'resnet18']
            elif compute_budget == 'medium':
                recommendations = ['resnet50', 'efficientnet_b3', 'vit_base_patch16_224']
            else:
                recommendations = ['efficientnet_b7', 'vit_large_patch16_224', 'swin_large']
        
        elif task_type == 'object_detection':
            recommendations = ['yolov5', 'faster_rcnn', 'retinanet', 'efficientdet']
        
        elif task_type == 'nlp':
            if dataset_size == 'small':
                recommendations = ['distilbert', 'albert_base', 'roberta_base']
            else:
                recommendations = ['bert_large', 'roberta_large', 'gpt2_medium']
        
        elif task_type == 'graph':
            recommendations = ['gcn', 'gat', 'graphsage', 'gin']
        
        elif task_type == 'time_series':
            recommendations = ['lstm', 'transformer', 'temporal_conv', 'neural_ode']
        
        print(f"\n[*] Architecture Recommendations")
        print(f"   Task: {task_type}")
        print(f"   Compute: {compute_budget}")
        print(f"   Recommendations: {len(recommendations)}")
        for arch in recommendations:
            print(f"     - {arch}")
        
        return recommendations


class AutoMLPipeline:
    """Pipeline AutoML completo"""
    
    def __init__(self):
        self.architect = AdvancedNeuralArchitect()
    
    def auto_design_architecture(self,
                                task: str,
                                input_shape: Tuple[int, ...],
                                output_dim: int,
                                trials: int = 50) -> nn.Module:
        """Design automatico architettura ottimale"""
        
        print(f"\n[*] AutoML Architecture Design")
        print(f"   Task: {task}")
        print(f"   Input shape: {input_shape}")
        print(f"   Output dim: {output_dim}")
        
        def objective(trial):
            # Sample architecture hyperparameters
            n_layers = trial.suggest_int('n_layers', 2, 8)
            hidden_dim = trial.suggest_categorical('hidden_dim', [64, 128, 256, 512])
            activation = trial.suggest_categorical('activation', ['relu', 'tanh', 'gelu'])
            dropout = trial.suggest_float('dropout', 0.1, 0.5)
            
            # Create model
            layers = []
            prev_dim = input_shape[-1]
            
            for i in range(n_layers):
                layers.append(nn.Linear(prev_dim, hidden_dim))
                if activation == 'relu':
                    layers.append(nn.ReLU())
                elif activation == 'tanh':
                    layers.append(nn.Tanh())
                else:
                    layers.append(nn.GELU())
                layers.append(nn.Dropout(dropout))
                prev_dim = hidden_dim
            
            layers.append(nn.Linear(prev_dim, output_dim))
            model = nn.Sequential(*layers)
            
            # Mock evaluation (in real scenario: train and evaluate)
            score = trial.number * 0.01  # Mock score
            
            return score
        
        # Run optimization
        result = self.architect.optimize_with_optuna(objective, n_trials=trials)
        
        # Build best model
        best_params = result['best_params']
        print(f"\n[OK] Best architecture found")
        print(f"   Layers: {best_params['n_layers']}")
        print(f"   Hidden dim: {best_params['hidden_dim']}")
        print(f"   Activation: {best_params['activation']}")
        
        return result


if __name__ == "__main__":
    print("Advanced Neural Architecture Designer - System Ready")
