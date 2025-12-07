
from core.brain import team, assign_task_to_team
from core.planner import create_plan
from tools.shell import install_program
from tools.files import extract_zip, perform_file_action

obiettivo = "Sviluppa un'app completa"
piano = {
    'goal': obiettivo,
    'steps': [
        "Progettazione UX",
        "Sviluppo frontend",
        "Sviluppo backend",
        "Test e QA",
        "Deploy e DevOps",
        "Documentazione",
        "Marketing e lancio"
    ],
    'skills': [
        "ux", "browser", "file", "qa", "devops", "documentazione", "marketing"
    ]
}
print(f"Obiettivo: {piano['goal']}")
print("Step:")
for step in piano['steps']:
    print(f"- {step}")

for i, (step, skill) in enumerate(zip(piano['steps'], piano['skills'])):
    agent_name = assign_task_to_team(step, priority=3+i, required_skill=skill)
    print(f"Task '{step}' assegnato a {agent_name} (skill: {skill})")

# Esempio: installazione pacchetto Python
print("\n[DevOps] Installa pacchetto 'requests'...")
result_install = install_program({'type': 'pip', 'name': 'requests'})
print("Installazione:", result_install)

# Esempio: estrazione ZIP
print("\n[QA] Estrae file ZIP...")
result_zip = extract_zip({'zip_path': 'test.zip', 'extract_to': './estratti'})
print("Estrazione ZIP:", result_zip)

# Esempio: operazioni avanzate su file
print("\n[File] Crea directory 'progetto'...")
result_mkdir = perform_file_action({'op': 'mkdir', 'path': 'progetto'})
print("Crea dir:", result_mkdir)

print("[File] Copia README.md in progetto/README.md...")
result_copy = perform_file_action({'op': 'copy', 'src': 'README.md', 'dst': 'progetto/README.md'})
print("Copia:", result_copy)

print("[File] Rinomina progetto/README.md in progetto/README_NEW.md...")
result_rename = perform_file_action({'op': 'rename', 'src': 'progetto/README.md', 'dst': 'progetto/README_NEW.md'})
print("Rinomina:", result_rename)

print("[File] Elimina progetto/README_NEW.md...")
result_delete = perform_file_action({'op': 'delete', 'path': 'progetto/README_NEW.md'})
print("Elimina:", result_delete)

team[3].propose_solution("Progettazione UX")
team[4].propose_solution("Deploy e DevOps")
team[5].correct_agent(team[1], "Testa meglio il frontend")
team[6].exchange_task(team[0], "Documentazione")

for agent in team:
    print(f"\nStato di {agent.name}:")
    print("Task:", agent.tasks)
    print("Log:", agent.log[-5:])
