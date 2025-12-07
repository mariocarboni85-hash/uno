from core.brain import team, assign_task_to_team
from tools.files import download_file, create_project_template, compress_files, generate_docs, analyze_code, monitor_directory
from tools.shell import install_program, update_dependencies, run_tests, send_notification, schedule_task

# 1. Download file da internet
print("[Downloader] Scarica requirements.txt...")
download_result = download_file({'url': 'https://raw.githubusercontent.com/pypa/pip/main/requirements.txt', 'dest': 'requirements.txt'})
print("Download:", download_result)

# 2. Aggiorna pip
print("[DevOps] Aggiorna pip...")
update_result = update_dependencies({'type': 'pip'})
print("Aggiornamento pip:", update_result)

# 3. Genera template progetto Python
print("[Project] Crea template Python...")
template_result = create_project_template({'type': 'python', 'path': 'progetto_auto'})
print("Template:", template_result)

# 4. Installa pacchetto 'pytest'
print("[DevOps] Installa pytest...")
install_result = install_program({'type': 'pip', 'name': 'pytest'})
print("Installazione:", install_result)

# 5. Esegui test automatici (mock)
print("[QA] Esegui test automatici...")
test_result = run_tests({'type': 'python', 'path': 'progetto_auto'})
print("Test:", test_result)

# 6. Comprimi progetto in ZIP
print("[Archiver] Comprimi progetto...")
compress_result = compress_files({'paths': ['progetto_auto/main.py', 'progetto_auto/requirements.txt'], 'zip_path': 'progetto_auto.zip'})
print("Compressione:", compress_result)

# 7. Genera documentazione automatica (mock)
print("[DocGen] Genera documentazione...")
doc_result = generate_docs({'source': 'progetto_auto/main.py', 'dest': 'progetto_auto/README_DOC.md'})
print("Documentazione:", doc_result)

# 8. Analisi statica del codice (mock)
print("[Analyzer] Analizza main.py...")
analysis_result = analyze_code({'path': 'progetto_auto/main.py'})
print("Analisi:", analysis_result)

# 9. Monitoraggio directory (mock)
print("[Monitor] Stato directory progetto_auto...")
monitor_result = monitor_directory({'path': 'progetto_auto'})
print("Monitoraggio:", monitor_result)

# 10. Invio notifica/email (mock)
print("[Notifier] Invio notifica...")
notif_result = send_notification({'to': 'team@app.com', 'subject': 'Workflow completato', 'body': 'Tutte le automazioni sono state eseguite.'})
print("Notifica:", notif_result)

# 11. Scheduling di task (mock)
print("[Scheduler] Schedulo test alle 23:00...")
sched_result = schedule_task({'cmd': 'pytest progetto_auto', 'time': '23:00'})
print("Scheduling:", sched_result)

# Stato finale agenti
for agent in team:
    print(f"\nStato di {agent.name}:")
    print("Task:", agent.tasks)
    print("Log:", agent.log[-5:])
