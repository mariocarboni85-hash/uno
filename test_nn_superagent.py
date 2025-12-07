import torch
from core.brain import AdvancedSuperAgentNN

# Test: training, predizione, valutazione, edge case

def test_nn_training():
    print("--- Test: Training rete neurale ---")
    X = torch.randn(100, 4)
    y = torch.randint(0, 3, (100,))
    nn_agent = AdvancedSuperAgentNN(input_size=4, hidden_sizes=[32, 16], output_size=3, dropout=0.1)
    loss = nn_agent.train_model(X, y, epochs=30, lr=0.01, classification=True, verbose=True)
    print(f"Loss finale: {loss:.4f}")

def test_nn_prediction():
    print("--- Test: Predizione rete neurale ---")
    X = torch.randn(10, 4)
    nn_agent = AdvancedSuperAgentNN(input_size=4, hidden_sizes=[32], output_size=3)
    pred = nn_agent.predict(X, classification=True)
    print(f"Predizioni: {pred.tolist()}")

def test_nn_evaluation():
    print("--- Test: Valutazione rete neurale ---")
    X = torch.randn(20, 4)
    y = torch.randint(0, 3, (20,))
    nn_agent = AdvancedSuperAgentNN(input_size=4, hidden_sizes=[32], output_size=3)
    nn_agent.train_model(X, y, epochs=10, lr=0.01, classification=True)
    metrics = nn_agent.evaluate(X, y, classification=True)
    print(f"Accuratezza: {metrics['accuracy']:.2f}")

def test_nn_batch_edge_case():
    print("--- Test: Edge case batch size 1 ---")
    X = torch.randn(1, 4)
    y = torch.randint(0, 3, (1,))
    nn_agent = AdvancedSuperAgentNN(input_size=4, hidden_sizes=[8], output_size=3)
    loss = nn_agent.train_model(X, y, epochs=5, lr=0.01, classification=True)
    print(f"Loss batch size 1: {loss:.4f}")

def test_nn_output_shape():
    print("--- Test: Output shape ---")
    X = torch.randn(5, 4)
    nn_agent = AdvancedSuperAgentNN(input_size=4, hidden_sizes=[8], output_size=3)
    out = nn_agent.forward(X)
    print(f"Output shape: {out.shape}")

if __name__ == "__main__":
    test_nn_training()
    test_nn_prediction()
    test_nn_evaluation()
    test_nn_batch_edge_case()
    test_nn_output_shape()
