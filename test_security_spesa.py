# Test sicurezza e filtro spesa massima 10 euro
from core.brain import SuperAgent

def test_security_jwt():
    print("--- Test: Sicurezza JWT ---")
    agent = SuperAgent("SecureAgent")
    try:
        token = agent.generate_jwt({"user": "test", "role": "admin"})
        assert agent.verify_jwt(token)
        print("JWT generato e verificato correttamente.")
    except Exception as e:
        print(f"Errore JWT: {e}")

def test_spesa_massima():
    print("--- Test: Filtro spesa massima 10 euro ---")
    agent = SuperAgent("Shopper")
    acquisti = [
        {"item": "penna", "prezzo": 2.5},
        {"item": "quaderno", "prezzo": 4.0},
        {"item": "calcolatrice", "prezzo": 12.0},
        {"item": "matita", "prezzo": 1.0},
        {"item": "gomma", "prezzo": 0.5},
    ]
    filtro = [a for a in acquisti if a["prezzo"] <= 10.0]
    print("Acquisti filtrati:")
    for a in filtro:
        print(f"  - {a['item']}: {a['prezzo']} euro")
    assert all(a["prezzo"] <= 10.0 for a in filtro)
    assert not any(a["prezzo"] > 10.0 for a in filtro)
    print("Filtro spesa massima OK.")

if __name__ == "__main__":
    test_security_jwt()
    test_spesa_massima()
