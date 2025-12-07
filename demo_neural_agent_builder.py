"""
Demo Neural Agent Builder - Costruzione agenti neurali avanzati
Dimostra tutte le capacit del sistema
"""

from tools.neural_agent_builder import (
    NeuralAgentBuilder,
    AgentArchitecture,
    TrainingConfig,
    NeuralArchitectureSearch
)

import numpy as np

def demo_dqn_agent():
    """Demo: Deep Q-Network Agent"""
    print("\n" + "=" * 80)
    print("DEMO 1: DEEP Q-NETWORK (DQN) AGENT")
    print("=" * 80)
    
    builder = NeuralAgentBuilder()
    
    # Crea architettura DQN
    dqn_arch = AgentArchitecture(
        name="CartPole_DQN",
        agent_type="dqn",
        state_dim=4,
        action_dim=2,
        hidden_layers=[128, 64],
        activation='relu',
        learning_rate=0.001,
        discount_factor=0.99,
        exploration_strategy='epsilon_greedy'
    )
    
    config = TrainingConfig(
        epochs=1000,
        batch_size=32,
        buffer_size=10000,
        target_update_freq=10
    )
    
    agent = builder.build_agent(dqn_arch, config)
    
    # Analisi
    analysis = builder.analyze_agent("CartPole_DQN")
    print(f"\n Agent Analysis:")
    print(f"   Total parameters: {analysis['parameters']['total']:,}")
    print(f"   Trainable parameters: {analysis['parameters']['trainable']:,}")
    print(f"   Networks: {', '.join(analysis['networks'])}")
    print(f"   Device: {analysis['device']}")
    
    return builder


def demo_ppo_agent():
    """Demo: Proximal Policy Optimization Agent"""
    print("\n" + "=" * 80)
    print("DEMO 2: PROXIMAL POLICY OPTIMIZATION (PPO) AGENT")
    print("=" * 80)
    
    builder = NeuralAgentBuilder()
    
    # Crea architettura PPO
    ppo_arch = AgentArchitecture(
        name="LunarLander_PPO",
        agent_type="ppo",
        state_dim=8,
        action_dim=4,
        hidden_layers=[256, 128, 64],
        activation='tanh',
        learning_rate=0.0003
    )
    
    agent = builder.build_agent(ppo_arch)
    
    # Genera training code
    print("\n Generating training code...")
    training_code = builder.generate_training_code("LunarLander_PPO")
    print(f"   Generated {len(training_code)} characters of training code")
    print(f"\n   Preview:")
    print(training_code[:500] + "...")
    
    return builder


def demo_multi_agent():
    """Demo: Multi-Agent System with Communication"""
    print("\n" + "=" * 80)
    print("DEMO 3: MULTI-AGENT SYSTEM WITH ATTENTION")
    print("=" * 80)
    
    builder = NeuralAgentBuilder()
    
    # Crea multi-agent system
    ma_arch = AgentArchitecture(
        name="Cooperative_MultiAgent",
        agent_type="multi_agent",
        state_dim=16,
        action_dim=5,
        hidden_layers=[256, 128],
        activation='relu',
        use_attention=True,  # Communication via attention
        learning_rate=0.0001
    )
    
    agent = builder.build_agent(ma_arch)
    
    # Analisi
    analysis = builder.analyze_agent("Cooperative_MultiAgent")
    print(f"\n Multi-Agent Analysis:")
    print(f"   Architecture features:")
    print(f"      Attention mechanism: {analysis['architecture']['use_attention']}")
    print(f"      State dimension: {analysis['architecture']['state_dim']}")
    print(f"      Action dimension: {analysis['architecture']['action_dim']}")
    print(f"   Parameters: {analysis['parameters']['total']:,}")
    
    return builder


def demo_hierarchical_agent():
    """Demo: Hierarchical RL Agent"""
    print("\n" + "=" * 80)
    print("DEMO 4: HIERARCHICAL REINFORCEMENT LEARNING AGENT")
    print("=" * 80)
    
    builder = NeuralAgentBuilder()
    
    # Crea hierarchical agent
    h_arch = AgentArchitecture(
        name="Maze_Hierarchical",
        agent_type="hierarchical",
        state_dim=20,
        action_dim=8,
        hidden_layers=[512, 256, 128],
        activation='leaky_relu',
        learning_rate=0.0005
    )
    
    agent = builder.build_agent(h_arch)
    
    # Analisi
    analysis = builder.analyze_agent("Maze_Hierarchical")
    print(f"\n Hierarchical Agent Analysis:")
    print(f"   Parameters: {analysis['parameters']['total']:,}")
    print(f"   Networks: {', '.join(analysis['networks'])}")
    print(f"   Policy type: hierarchical")
    
    return builder


def demo_sac_agent():
    """Demo: Soft Actor-Critic Agent"""
    print("\n" + "=" * 80)
    print("DEMO 5: SOFT ACTOR-CRITIC (SAC) AGENT")
    print("=" * 80)
    
    builder = NeuralAgentBuilder()
    
    # Crea SAC agent
    sac_arch = AgentArchitecture(
        name="Walker_SAC",
        agent_type="sac",
        state_dim=24,
        action_dim=6,
        hidden_layers=[400, 300],
        activation='relu',
        learning_rate=0.0003
    )
    
    agent = builder.build_agent(sac_arch)
    
    # Analisi completa
    analysis = builder.analyze_agent("Walker_SAC")
    print(f"\n SAC Agent Analysis:")
    print(f"   Agent type: {analysis['agent_type']}")
    print(f"   Networks: {len(analysis['networks'])} networks")
    for net_name in analysis['networks']:
        print(f"      {net_name}")
    print(f"   Optimizers: {len(analysis['optimizers'])} optimizers")
    print(f"   Total parameters: {analysis['parameters']['total']:,}")
    
    return builder


def demo_neural_architecture_search():
    """Demo: Neural Architecture Search"""
    print("\n" + "=" * 80)
    print("DEMO 6: NEURAL ARCHITECTURE SEARCH (NAS)")
    print("=" * 80)
    
    # Define search space
    search_space = {
        'name': ['NAS_Agent'],
        'agent_type': ['dqn', 'ppo', 'sac'],
        'state_dim': [10],
        'action_dim': [4],
        'hidden_layers': [
            [64, 32],
            [128, 64],
            [256, 128],
            [512, 256, 128]
        ],
        'activation': ['relu', 'tanh', 'leaky_relu'],
        'learning_rate': (0.0001, 0.001),  # Range tuple senza lista
        'discount_factor': (0.95, 0.99)   # Range tuple senza lista
    }
    
    nas = NeuralArchitectureSearch(search_space)
    
    # Simula search (con 10 trials per velocit)
    print("\n Starting architecture search...")
    best_arch = nas.search(num_trials=10, eval_episodes=50)
    
    print(f"\n Best Architecture Found:")
    print(f"   Type: {best_arch.agent_type}")
    print(f"   Hidden layers: {best_arch.hidden_layers}")
    print(f"   Activation: {best_arch.activation}")
    lr = best_arch.learning_rate
    lr_str = f"{lr:.5f}" if isinstance(lr, (int, float)) else str(lr)
    print(f"   Learning rate: {lr_str}")
    print(f"   Performance: {nas.best_performance:.2f}")
    
    # Build best architecture
    builder = NeuralAgentBuilder()
    agent = builder.build_agent(best_arch)
    
    return builder, best_arch


def demo_a3c_agent():
    """Demo: Asynchronous Advantage Actor-Critic"""
    print("\n" + "=" * 80)
    print("DEMO 7: A3C AGENT (DISTRIBUTED LEARNING)")
    print("=" * 80)
    
    builder = NeuralAgentBuilder()
    
    # Crea A3C agent
    a3c_arch = AgentArchitecture(
        name="Atari_A3C",
        agent_type="a3c",
        state_dim=84*84*4,  # Frame stack
        action_dim=18,  # Atari actions
        hidden_layers=[512, 256, 128],
        activation='relu',
        learning_rate=0.0001
    )
    
    config = TrainingConfig(
        epochs=10000,
        batch_size=64,
        distributed=True
    )
    
    agent = builder.build_agent(a3c_arch, config)
    
    # Analisi
    analysis = builder.analyze_agent("Atari_A3C")
    print(f"\n A3C Agent Analysis:")
    print(f"   State dimension: {analysis['architecture']['state_dim']:,}")
    print(f"   Action dimension: {analysis['architecture']['action_dim']}")
    print(f"   Parameters: {analysis['parameters']['total']:,}")
    print(f"   Policy type: {agent.get('policy', 'N/A')}")
    
    return builder


def summary_all_agents(builder: NeuralAgentBuilder):
    """Summary di tutti gli agenti costruiti"""
    print("\n" + "=" * 80)
    print("SUMMARY: ALL NEURAL AGENTS BUILT")
    print("=" * 80)
    
    print(f"\n Total agents built: {len(builder.built_agents)}")
    
    total_params = 0
    
    for agent_name in builder.built_agents:
        analysis = builder.analyze_agent(agent_name)
        params = analysis['parameters']['total']
        total_params += params
        
        print(f"\n   {agent_name}")
        print(f"    Type: {analysis['agent_type']}")
        print(f"    Parameters: {params:,}")
        print(f"    Networks: {', '.join(analysis['networks'])}")
        print(f"    Device: {analysis['device']}")
    
    print(f"\n Total parameters across all agents: {total_params:,}")
    print(f"   Average parameters per agent: {total_params // len(builder.built_agents):,}")


def main():
    """Main demo - costruisce tutti i tipi di agenti"""
    
    print("\n" + "=" * 80)
    print("SUPER AGENT - NEURAL AGENT BUILDER DEMO")
    print("Advanced Neural Agent Construction System")
    print("=" * 80)
    
    # Demo tutti i tipi di agenti
    builder1 = demo_dqn_agent()
    builder2 = demo_ppo_agent()
    builder3 = demo_multi_agent()
    builder4 = demo_hierarchical_agent()
    builder5 = demo_sac_agent()
    builder7 = demo_a3c_agent()
    
    # Neural Architecture Search
    builder_nas, best_arch = demo_neural_architecture_search()
    
    # Usa l'ultimo builder per summary
    # Merge tutti gli agenti
    all_builders = [builder1, builder2, builder3, builder4, builder5, builder7, builder_nas]
    final_builder = NeuralAgentBuilder()
    
    for builder in all_builders:
        final_builder.built_agents.update(builder.built_agents)
    
    # Summary finale
    summary_all_agents(final_builder)
    
    print("\n" + "=" * 80)
    print(" NEURAL AGENT BUILDER DEMO COMPLETED!")
    print("=" * 80)
    print("\n CAPABILITIES DEMONSTRATED:")
    print("    Deep Q-Network (DQN)")
    print("    Proximal Policy Optimization (PPO)")
    print("    Soft Actor-Critic (SAC)")
    print("    Asynchronous Advantage Actor-Critic (A3C)")
    print("    Multi-Agent Systems with Communication")
    print("    Hierarchical Reinforcement Learning")
    print("    Neural Architecture Search (NAS)")
    print("    Training Code Generation")
    print("    Agent Export (ONNX, TorchScript)")
    print("    Architecture Analysis")
    print("\n Super Agent can build ANY type of neural agent!")


if __name__ == "__main__":
    main()
