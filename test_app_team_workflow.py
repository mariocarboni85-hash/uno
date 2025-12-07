from core.brain import team, assign_task_to_team
from core.planner import create_plan

# 1. Definisci l'obiettivo
obiettivo = "Sviluppa un'app"

# 2. Crea piano multi-step
piano = create_plan(obiettivo)
print(f"Obiettivo: {piano['goal']}")
print("Step:")
for step in piano['steps']:
    print(f"- {step}")

# 3. Assegna i task agli agenti in base alle skill
step_skill_map = [
    ("Progettazione app", "planner"),
    ("Sviluppo frontend", "browser"),
    ("Sviluppo backend", "file"),
    ("Test e verifica", "shell")
]
for i, (step, skill) in enumerate(step_skill_map):
    agent_name = assign_task_to_team(step, priority=3+i, required_skill=skill)
    print(f"Task '{step}' assegnato a {agent_name} (skill: {skill})")

# 4. Simula collaborazione e feedback
team[0].propose_solution("Progettazione app")
team[1].correct_agent(team[2], "Ottimizza la struttura backend")
team[2].exchange_task(team[0], "Sviluppo backend")

# 5. Mostra stato finale
for agent in team:
    print(f"\nStato di {agent.name}:")
    print("Task:", agent.tasks)
    print("Log:", agent.log[-5:])
