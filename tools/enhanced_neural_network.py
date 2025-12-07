"""
Enhanced Neural Network for Super Agent
Architettura avanzata con Memory Networks, Attention, Meta-Learning
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
from dataclasses import dataclass
import json
from pathlib import Path


@dataclass
class NeuralConfig:
    """Configurazione rete neurale Super Agent"""
    input_dim: int = 512
    hidden_dims: List[int] = None
    output_dim: int = 256
    num_heads: int = 8
    num_layers: int = 6
    dropout: float = 0.1
    memory_size: int = 1000
    use_attention: bool = True
    use_memory: bool = True
    use_residual: bool = True
    activation: str = 'gelu'
    
    def __post_init__(self):
        if self.hidden_dims is None:
            self.hidden_dims = [1024, 512, 256]


class MultiHeadSelfAttention(nn.Module):
    """Multi-Head Self-Attention mechanism"""
    
    def __init__(self, dim: int, num_heads: int = 8, dropout: float = 0.1):
        super().__init__()
        assert dim % num_heads == 0, "dim must be divisible by num_heads"
        
        self.dim = dim
        self.num_heads = num_heads
        self.head_dim = dim // num_heads
        self.scale = self.head_dim ** -0.5
        
        self.qkv = nn.Linear(dim, dim * 3, bias=False)
        self.proj = nn.Linear(dim, dim)
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, x: torch.Tensor, mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        B, N, C = x.shape
        
        # Generate Q, K, V
        qkv = self.qkv(x).reshape(B, N, 3, self.num_heads, self.head_dim).permute(2, 0, 3, 1, 4)
        q, k, v = qkv[0], qkv[1], qkv[2]
        
        # Scaled dot-product attention
        attn = (q @ k.transpose(-2, -1)) * self.scale
        
        if mask is not None:
            attn = attn.masked_fill(mask == 0, float('-inf'))
        
        attn = F.softmax(attn, dim=-1)
        attn = self.dropout(attn)
        
        # Combine with values
        x = (attn @ v).transpose(1, 2).reshape(B, N, C)
        x = self.proj(x)
        x = self.dropout(x)
        
        return x


class FeedForward(nn.Module):
    """Position-wise Feed-Forward Network"""
    
    def __init__(self, dim: int, hidden_dim: int, dropout: float = 0.1, activation: str = 'gelu'):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(dim, hidden_dim),
            nn.GELU() if activation == 'gelu' else nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, dim),
            nn.Dropout(dropout)
        )
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class TransformerBlock(nn.Module):
    """Transformer block with attention and feed-forward"""
    
    def __init__(self, dim: int, num_heads: int, mlp_ratio: float = 4.0, 
                 dropout: float = 0.1, activation: str = 'gelu'):
        super().__init__()
        
        self.norm1 = nn.LayerNorm(dim)
        self.attn = MultiHeadSelfAttention(dim, num_heads, dropout)
        self.norm2 = nn.LayerNorm(dim)
        self.mlp = FeedForward(dim, int(dim * mlp_ratio), dropout, activation)
        
    def forward(self, x: torch.Tensor, mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        # Attention with residual
        x = x + self.attn(self.norm1(x), mask)
        
        # Feed-forward with residual
        x = x + self.mlp(self.norm2(x))
        
        return x


class MemoryNetwork(nn.Module):
    """Neural Memory Network per context storage"""
    
    def __init__(self, memory_size: int, dim: int):
        super().__init__()
        self.memory_size = memory_size
        self.dim = dim
        
        # Memory slots
        self.memory_keys = nn.Parameter(torch.randn(memory_size, dim))
        self.memory_values = nn.Parameter(torch.randn(memory_size, dim))
        
        # Query projection
        self.query_proj = nn.Linear(dim, dim)
        
    def forward(self, query: torch.Tensor) -> torch.Tensor:
        """
        Args:
            query: (B, dim)
        Returns:
            retrieved: (B, dim)
        """
        B = query.size(0)
        
        # Project query
        q = self.query_proj(query)  # (B, dim)
        
        # Compute attention scores
        scores = torch.matmul(q, self.memory_keys.t())  # (B, memory_size)
        attn_weights = F.softmax(scores, dim=-1)  # (B, memory_size)
        
        # Retrieve from memory
        retrieved = torch.matmul(attn_weights, self.memory_values)  # (B, dim)
        
        return retrieved
    
    def update_memory(self, index: int, key: torch.Tensor, value: torch.Tensor):
        """Update specific memory slot"""
        with torch.no_grad():
            self.memory_keys[index] = key
            self.memory_values[index] = value


class MetaLearningLayer(nn.Module):
    """Meta-learning layer for fast adaptation"""
    
    def __init__(self, dim: int, num_inner_steps: int = 5, inner_lr: float = 0.01):
        super().__init__()
        self.dim = dim
        self.num_inner_steps = num_inner_steps
        self.inner_lr = inner_lr
        
        # Task-specific adaptation parameters
        self.task_embedding = nn.Parameter(torch.randn(1, dim))
        self.adaptation_layer = nn.Linear(dim, dim)
        
    def forward(self, x: torch.Tensor, task_context: Optional[torch.Tensor] = None) -> torch.Tensor:
        """
        Args:
            x: (B, dim)
            task_context: Optional task-specific context
        Returns:
            adapted: (B, dim)
        """
        if task_context is not None:
            # Adapt to specific task
            task_emb = task_context
        else:
            # Use default task embedding
            task_emb = self.task_embedding.expand(x.size(0), -1)
        
        # Combine input with task embedding
        combined = x + task_emb
        adapted = self.adaptation_layer(combined)
        
        return adapted


class EnhancedSuperAgentNetwork(nn.Module):
    """
    Enhanced Neural Network for Super Agent
    Features:
    - Multi-Head Self-Attention
    - Memory Networks
    - Meta-Learning
    - Residual connections
    - Layer normalization
    """
    
    def __init__(self, config: NeuralConfig):
        super().__init__()
        self.config = config
        
        # Input projection
        self.input_proj = nn.Linear(config.input_dim, config.hidden_dims[0])
        
        # Transformer blocks
        self.transformer_blocks = nn.ModuleList([
            TransformerBlock(
                dim=config.hidden_dims[0],
                num_heads=config.num_heads,
                dropout=config.dropout,
                activation=config.activation
            )
            for _ in range(config.num_layers)
        ])
        
        # Memory network
        if config.use_memory:
            self.memory_network = MemoryNetwork(
                memory_size=config.memory_size,
                dim=config.hidden_dims[0]
            )
        
        # Meta-learning layer
        self.meta_learning = MetaLearningLayer(config.hidden_dims[0])
        
        # Hidden layers with residual connections
        self.hidden_layers = nn.ModuleList()
        prev_dim = config.hidden_dims[0]
        
        for hidden_dim in config.hidden_dims[1:]:
            self.hidden_layers.append(nn.Sequential(
                nn.Linear(prev_dim, hidden_dim),
                nn.LayerNorm(hidden_dim),
                nn.GELU() if config.activation == 'gelu' else nn.ReLU(),
                nn.Dropout(config.dropout)
            ))
            prev_dim = hidden_dim
        
        # Output projection
        self.output_proj = nn.Linear(prev_dim, config.output_dim)
        
        # Final layer norm
        self.final_norm = nn.LayerNorm(config.output_dim)
        
        self._init_weights()
    
    def _init_weights(self):
        """Initialize weights with Xavier/Kaiming"""
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.xavier_uniform_(module.weight)
                if module.bias is not None:
                    nn.init.zeros_(module.bias)
            elif isinstance(module, nn.LayerNorm):
                nn.init.ones_(module.weight)
                nn.init.zeros_(module.bias)
    
    def forward(self, x: torch.Tensor, 
                task_context: Optional[torch.Tensor] = None,
                use_memory: bool = True) -> Dict[str, torch.Tensor]:
        """
        Forward pass
        
        Args:
            x: Input tensor (B, input_dim) or (B, N, input_dim)
            task_context: Optional task-specific context
            use_memory: Whether to use memory network
            
        Returns:
            Dictionary with output and attention weights
        """
        # Handle different input shapes
        if x.dim() == 2:
            x = x.unsqueeze(1)  # (B, 1, input_dim)
        
        B, N, _ = x.shape
        
        # Input projection
        x = self.input_proj(x)  # (B, N, hidden_dim)
        
        # Transformer blocks with residual
        attention_weights = []
        for transformer in self.transformer_blocks:
            x = transformer(x)
        
        # Pool sequence dimension (mean pooling)
        x = x.mean(dim=1)  # (B, hidden_dim)
        
        # Memory network
        if self.config.use_memory and use_memory:
            memory_output = self.memory_network(x)
            x = x + memory_output  # Residual connection
        
        # Meta-learning adaptation
        x = self.meta_learning(x, task_context)
        
        # Hidden layers with residual
        for layer in self.hidden_layers:
            identity = x
            x = layer(x)
            
            # Residual connection if dimensions match
            if identity.size(-1) == x.size(-1):
                x = x + identity
        
        # Output projection
        output = self.output_proj(x)
        output = self.final_norm(output)
        
        return {
            'output': output,
            'features': x,
            'attention_weights': attention_weights
        }
    
    def get_attention_maps(self) -> List[torch.Tensor]:
        """Extract attention maps from transformer blocks"""
        attention_maps = []
        for block in self.transformer_blocks:
            if hasattr(block.attn, 'attention_weights'):
                attention_maps.append(block.attn.attention_weights)
        return attention_maps


class SuperAgentEmbedding(nn.Module):
    """Embedding layer per input multi-modali"""
    
    def __init__(self, vocab_sizes: Dict[str, int], embedding_dim: int):
        super().__init__()
        self.embeddings = nn.ModuleDict({
            name: nn.Embedding(vocab_size, embedding_dim)
            for name, vocab_size in vocab_sizes.items()
        })
        
    def forward(self, inputs: Dict[str, torch.Tensor]) -> torch.Tensor:
        """
        Args:
            inputs: Dictionary of input tensors for each modality
        Returns:
            Combined embeddings (B, embedding_dim)
        """
        embedded = []
        for name, input_tensor in inputs.items():
            if name in self.embeddings:
                emb = self.embeddings[name](input_tensor)
                embedded.append(emb)
        
        # Combine embeddings (mean pooling)
        if embedded:
            return torch.stack(embedded).mean(dim=0)
        else:
            return torch.zeros(1, 1)  # Fallback


class SuperAgentEncoder(nn.Module):
    """Encoder per diversi tipi di input"""
    
    def __init__(self, input_types: Dict[str, int], output_dim: int):
        super().__init__()
        
        self.encoders = nn.ModuleDict()
        
        for input_type, input_dim in input_types.items():
            self.encoders[input_type] = nn.Sequential(
                nn.Linear(input_dim, output_dim * 2),
                nn.GELU(),
                nn.LayerNorm(output_dim * 2),
                nn.Dropout(0.1),
                nn.Linear(output_dim * 2, output_dim),
                nn.LayerNorm(output_dim)
            )
    
    def forward(self, inputs: Dict[str, torch.Tensor]) -> torch.Tensor:
        """
        Args:
            inputs: Dictionary of tensors for each input type
        Returns:
            Encoded representation (B, output_dim)
        """
        encoded = []
        
        for input_type, tensor in inputs.items():
            if input_type in self.encoders:
                enc = self.encoders[input_type](tensor)
                encoded.append(enc)
        
        # Combine encodings
        if encoded:
            return torch.stack(encoded).mean(dim=0)
        else:
            return torch.zeros(1, list(self.encoders.values())[0][0].out_features)


class SuperAgentNeuralSystem:
    """Sistema neurale completo per Super Agent"""
    
    def __init__(self, config: NeuralConfig = None, device: str = 'cpu'):
        if config is None:
            config = NeuralConfig()
        
        self.config = config
        self.device = torch.device(device)
        
        # Main network
        self.network = EnhancedSuperAgentNetwork(config).to(self.device)
        
        # Optimizer
        self.optimizer = torch.optim.AdamW(
            self.network.parameters(),
            lr=1e-4,
            betas=(0.9, 0.999),
            weight_decay=0.01
        )
        
        # Learning rate scheduler
        self.scheduler = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(
            self.optimizer,
            T_0=10,
            T_mult=2
        )
        
        self.training_history = []
        
    def forward(self, x: torch.Tensor, **kwargs) -> Dict[str, torch.Tensor]:
        """Forward pass through network"""
        if not isinstance(x, torch.Tensor):
            x = torch.tensor(x, dtype=torch.float32)
        
        x = x.to(self.device)
        return self.network(x, **kwargs)
    
    def train_step(self, x: torch.Tensor, y: torch.Tensor) -> float:
        """Single training step"""
        self.network.train()
        
        x = x.to(self.device)
        y = y.to(self.device)
        
        # Forward pass
        output = self.network(x)['output']
        
        # Compute loss
        loss = F.mse_loss(output, y)
        
        # Backward pass
        self.optimizer.zero_grad()
        loss.backward()
        
        # Gradient clipping
        torch.nn.utils.clip_grad_norm_(self.network.parameters(), max_norm=1.0)
        
        self.optimizer.step()
        self.scheduler.step()
        
        return loss.item()
    
    def evaluate(self, x: torch.Tensor, y: torch.Tensor) -> Dict[str, float]:
        """Evaluate model"""
        self.network.eval()
        
        with torch.no_grad():
            x = x.to(self.device)
            y = y.to(self.device)
            
            output = self.network(x)['output']
            
            mse_loss = F.mse_loss(output, y).item()
            mae_loss = F.l1_loss(output, y).item()
        
        return {
            'mse_loss': mse_loss,
            'mae_loss': mae_loss
        }
    
    def save_model(self, path: str):
        """Save model checkpoint"""
        checkpoint = {
            'config': self.config,
            'model_state_dict': self.network.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict(),
            'training_history': self.training_history
        }
        torch.save(checkpoint, path)
        print(f"[OK] Model saved to {path}")
    
    def load_model(self, path: str):
        """Load model checkpoint"""
        checkpoint = torch.load(path, map_location=self.device, weights_only=False)
        
        self.config = checkpoint['config']
        self.network.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
        self.training_history = checkpoint['training_history']
        
        print(f"[OK] Model loaded from {path}")
    
    def get_model_summary(self) -> Dict[str, Any]:
        """Get model architecture summary"""
        total_params = sum(p.numel() for p in self.network.parameters())
        trainable_params = sum(p.numel() for p in self.network.parameters() if p.requires_grad)
        
        return {
            'total_parameters': total_params,
            'trainable_parameters': trainable_params,
            'config': self.config,
            'device': str(self.device),
            'layers': len(list(self.network.modules())),
            'optimizer': self.optimizer.__class__.__name__,
            'scheduler': self.scheduler.__class__.__name__
        }
    
    def analyze_attention(self, x: torch.Tensor) -> Dict[str, Any]:
        """Analyze attention patterns"""
        self.network.eval()
        
        with torch.no_grad():
            x = x.to(self.device)
            output = self.network(x)
            
            attention_maps = self.network.get_attention_maps()
        
        return {
            'num_attention_layers': len(attention_maps),
            'attention_shapes': [map.shape for map in attention_maps] if attention_maps else [],
            'output_shape': output['output'].shape
        }


def create_enhanced_network(
    input_dim: int = 512,
    output_dim: int = 256,
    num_heads: int = 8,
    num_layers: int = 6,
    memory_size: int = 1000
) -> SuperAgentNeuralSystem:
    """Factory function per creare rete enhanced"""
    
    config = NeuralConfig(
        input_dim=input_dim,
        hidden_dims=[1024, 512, 256],
        output_dim=output_dim,
        num_heads=num_heads,
        num_layers=num_layers,
        dropout=0.1,
        memory_size=memory_size,
        use_attention=True,
        use_memory=True,
        use_residual=True,
        activation='gelu'
    )
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    system = SuperAgentNeuralSystem(config, device)
    
    print(f"\n[*] Enhanced Neural Network Created")
    summary = system.get_model_summary()
    print(f"   Total parameters: {summary['total_parameters']:,}")
    print(f"   Trainable parameters: {summary['trainable_parameters']:,}")
    print(f"   Layers: {summary['layers']}")
    print(f"   Device: {summary['device']}")
    print(f"   Attention heads: {num_heads}")
    print(f"   Transformer layers: {num_layers}")
    print(f"   Memory size: {memory_size}")
    
    return system


if __name__ == "__main__":
    print("Enhanced Neural Network for Super Agent")
    print("=" * 80)
    
    # Create network
    system = create_enhanced_network(
        input_dim=512,
        output_dim=256,
        num_heads=8,
        num_layers=6,
        memory_size=1000
    )
    
    # Test forward pass
    x = torch.randn(32, 512)
    output = system.forward(x)
    
    print(f"\n[*] Test Forward Pass")
    print(f"   Input shape: {x.shape}")
    print(f"   Output shape: {output['output'].shape}")
    print(f"   Features shape: {output['features'].shape}")
    
    print("\n[OK] Enhanced Neural Network ready!")
