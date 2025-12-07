import unittest
from core.brain import SuperAgent

class TestSuperAgentUpgrade(unittest.TestCase):
    def setUp(self):
        self.agent = SuperAgent("TestAgent", skills=["informatica", "meccanica", "elettrica", "fisica"])

    def test_propose_solution_informatica(self):
        result = self.agent.propose_solution("Trova il bug in un algoritmo", "informatica")
        self.assertIn("bug individuato", result)

    def test_propose_solution_meccanica(self):
        result = self.agent.propose_solution("Calcola l'integrale di x^2 da 0 a 2", "meccanica")
        self.assertIn("Integrale x^2", result)

    def test_propose_solution_elettrica(self):
        result = self.agent.propose_solution("Calcola la resistenza equivalente di tre resistenze", "elettrica")
        self.assertIn("Resistenza equivalente", result)

    def test_propose_solution_fisica(self):
        result = self.agent.propose_solution("Simula il moto parabolico di un oggetto", "fisica")
        self.assertIn("Simulazione moto parabolico", result)

    def test_logging(self):
        self.agent.propose_solution("Trova il bug in un algoritmo", "informatica")
        self.assertTrue(any("bug individuato" in log for log in self.agent.log))

if __name__ == "__main__":
    unittest.main()
