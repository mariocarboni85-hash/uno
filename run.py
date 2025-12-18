"""Demo runner for the uno project."""
import sys
import os
from datetime import datetime
from agent import uno
from tools import shell, files, browser
from core.team import TeamCoordinator, AgentProfile
from core.factory import create_agent_package

try:
    from tools import arduino
    ARDUINO_AVAILABLE = arduino.is_cli_installed()
except:
    ARDUINO_AVAILABLE = False

TOOLS = {
    'shell': shell.run,
    'files_write': files.write_file,
    'files_read': files.read_file,
    'list_dir': files.list_dir,
    'browser': browser.fetch,
}

if ARDUINO_AVAILABLE:
    TOOLS['arduino_compile'] = arduino.compile_sketch
    TOOLS['arduino_upload'] = arduino.upload_sketch
    TOOLS['arduino_list'] = arduino.list_boards


def demo_planner():
    """Demo della modalità planner automatico."""
    print("=== uno Demo: Modalità Planner ===")
    agent = uno(TOOLS, name="PlannerAgent")
    agent.run('create a file, then run a command')


def interactive_mode():
    """Demo della modalità interattiva con LLM."""
    print("=== uno Demo: Modalità Interattiva ===")
    print("Digita 'exit' o 'quit' per uscire.\n")
    
    agent = uno(TOOLS, name="InteractiveAgent")
    
    while True:
        try:
            user_input = input("Tu: ")
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("Arrivederci!")
                break
            
            output = agent.ask(user_input)
            print(f"\nAGENTE: {output}\n")
        except KeyboardInterrupt:
            print("\n\nInterrotto dall'utente.")
            break
        except Exception as e:
            print(f"\nErrore: {e}\n")


def _run_build_interactive():
    """Flusso interattivo per costruire un agente custom."""
    print("=== SuperAgent: Costruzione agente custom ===")
    name = input("Nome tecnico agente (es. supporto_clienti): ").strip() or "custom_agent"
    title = input("Titolo leggibile (es. Agente Supporto Clienti): ").strip() or name
    description = input("Breve descrizione: ").strip() or "Agente custom generato da SuperAgent."

    # Setup team
    coordinator = TeamCoordinator(TOOLS)
    coordinator.add_profile(AgentProfile(
        name="RequirementsAgent", role="requirements",
        system_prompt="Analista requisiti per agenti software"
    ))
    coordinator.add_profile(AgentProfile(
        name="DesignAgent", role="design",
        system_prompt="Architetto di agenti AI modulari"
    ))
    coordinator.add_profile(AgentProfile(
        name="ImplementationAgent", role="implementation",
        system_prompt="Sviluppatore Python specializzato in agenti"
    ))
    coordinator.build_agents()

    spec_text = f"Nome: {name}\nTitolo: {title}\nDescrizione: {description}"
    artifacts = coordinator.run_build_flow(spec_text)

    print("\n--- Requisiti generati ---\n")
    print(artifacts.get("requirements", "(nessuno)"))
    print("\n--- Design proposto ---\n")
    print(artifacts.get("design", "(nessuno)"))
    print("\n--- Piano file ---\n")
    print(artifacts.get("files_plan", "(nessuno)"))

    package_path = create_agent_package({
        "name": name,
        "title": title,
        "description": description,
    }, files_plan=artifacts.get("files_plan"))

    print(f"\nPacchetto agente creato in: {package_path}")
    print("Puoi zipparlo e venderlo / distribuirlo.")


def _run_build_preset(preset: str):
    """Costruisce un agente da preset noto (nessuna domanda interattiva)."""
    if preset == "supporto_clienti":
        spec = {
            "name": "supporto_clienti",
            "title": "Agente Supporto Clienti",
            "description": "Agente per rispondere a email/FAQ in italiano usando file FAQ locali.",
        }
        files_plan = (
            "prompts/system_prompt.txt - prompt di sistema per agente supporto clienti in italiano\n"
            "config/support_config.py - configurazione modelli e parametri per supporto clienti\n"
            "tools/faq_loader.py - stub per caricare e cercare nelle FAQ locali\n"
            "docs/usage.md - istruzioni per usare l'agente di supporto clienti\n"
        )
    elif preset == "devops_shell_sicuro":
        spec = {
            "name": "devops_shell_sicuro",
            "title": "Agente DevOps Shell Sicuro",
            "description": "Agente per eseguire comandi shell con filtri di sicurezza e log.",
        }
        files_plan = (
            "prompts/system_prompt.txt - prompt di sistema per agente devops con focus sicurezza\n"
            "config/devops_config.py - configurazione modelli e limiti di sicurezza\n"
            "tools/safe_shell.py - wrapper per comandi shell con filtri di sicurezza\n"
            "docs/usage.md - guida per usare l'agente DevOps in modo sicuro\n"
        )
    elif preset == "analista_requisiti":
        spec = {
            "name": "analista_requisiti",
            "title": "Agente Analista Requisiti",
            "description": "Agente che trasforma richieste vaghe in specifiche chiare e strutturate.",
        }
        files_plan = (
            "prompts/system_prompt.txt - prompt di sistema per analisi requisiti software\n"
            "config/requirements_config.py - configurazione generica per analisi requisiti\n"
            "docs/usage.md - istruzioni per usare l'agente analista requisiti\n"
        )
    elif preset == "copy_marketing":
        spec = {
            "name": "copy_marketing",
            "title": "Agente Copy Marketing",
            "description": "Agente per generare testi marketing (email, landing, social) in italiano.",
        }
        files_plan = (
            "prompts/system_prompt.txt - prompt di sistema per copywriter marketing in italiano\n"
            "config/marketing_config.py - configurazione modelli e toni di voce\n"
            "docs/usage.md - istruzioni per usare l'agente copy marketing\n"
        )
    else:
        print(f"Preset sconosciuto: {preset}")
        return

    print(f"=== SuperAgent: Costruzione agente preset '{preset}' ===")
    package_path = create_agent_package(spec, files_plan=files_plan)
    print(f"Pacchetto agente creato in: {package_path}")
    print("Puoi zipparlo e venderlo / distribuirlo.")


def main():
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        mode = None

    if mode == '--interactive':
        interactive_mode()
    elif mode == '--build-agent':
        # modalità interattiva standard
        _run_build_interactive()
    elif mode == '--build-agent-preset' and len(sys.argv) > 2:
        # es: python run.py --build-agent-preset supporto_clienti
        _run_build_preset(sys.argv[2])
    elif mode == '--improve-agent':
        # Modalità: il team analizza e migliora un agente esistente
        print("=== SuperAgent: Revisione agente esistente ===")
        print("Incolla o descrivi l'agente (scopo, prompt, tools, problemi).\n")
        print("Termina con una riga contenente solo 'FINE' e premi Invio.\n")

        lines = []
        while True:
            line = input()
            if line.strip().upper() == 'FINE':
                break
            lines.append(line)

        description = "\n".join(lines).strip()
        if not description:
            print("Nessuna descrizione fornita. Uscita.")
            return

        coordinator = TeamCoordinator(TOOLS)
        coordinator.add_profile(AgentProfile(
            name="RequirementsAgent", role="requirements",
            system_prompt="Analista requisiti per agenti AI esistenti"
        ))
        coordinator.add_profile(AgentProfile(
            name="DesignAgent", role="design",
            system_prompt="Architetto di agenti AI che progetta miglioramenti strutturali"
        ))
        coordinator.add_profile(AgentProfile(
            name="QAReviewerAgent", role="qa",
            system_prompt=(
                "QA Reviewer che valuta la qualità e l'affidabilità di agenti AI "
                "e propone checklist di miglioramento pratiche"
            ),
        ))
        coordinator.build_agents()

        review = coordinator.review_existing_agent(description)

        print("\n--- Problemi individuati ---\n")
        print(review.get("issues", "(nessuno)"))
        print("\n--- Miglioramenti proposti ---\n")
        print(review.get("improvements", "(nessuno)"))
        print("\n--- Rischi e failure mode ---\n")
        print(review.get("risks", "(nessuno)"))
        print("\n--- QA Checklist ---\n")
        print(review.get("qa_feedback", "(nessuna)"))

        # Salva automaticamente la revisione in agent_reviews/
        reviews_dir = os.path.join(os.path.dirname(__file__), "agent_reviews")
        os.makedirs(reviews_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"review_{timestamp}.md"
        review_path = os.path.join(reviews_dir, filename)

        try:
            with open(review_path, "w", encoding="utf-8") as f:
                f.write("# Revisione agente\n\n")
                f.write("## Descrizione iniziale\n\n")
                f.write(description + "\n\n")
                f.write("## Problemi individuati\n\n")
                f.write(review.get("issues", "(nessuno)") + "\n\n")
                f.write("## Miglioramenti proposti\n\n")
                f.write(review.get("improvements", "(nessuno)") + "\n\n")
                f.write("## Rischi e failure mode\n\n")
                f.write(review.get("risks", "(nessuno)") + "\n\n")
                f.write("## QA Checklist\n\n")
                f.write(review.get("qa_feedback", "(nessuna)") + "\n")
            print(f"\nRevisione salvata in: {review_path}")
        except Exception as e:
            print(f"\nImpossibile salvare la revisione su file ({e}).")
    elif mode == '--team-demo':
        # Demo semplice di collaborazione tra agenti
        print("=== SuperAgent: Team Demo ===")
        user_issue = input("Descrivi un problema da analizzare: ")

        coordinator = TeamCoordinator(TOOLS)
        coordinator.add_profile(AgentProfile(
            name="RequirementsAgent", role="requirements",
            system_prompt="Analista requisiti per problemi complessi"
        ))
        coordinator.add_profile(AgentProfile(
            name="DesignAgent", role="design",
            system_prompt="Architetto di soluzioni AI/software"
        ))
        coordinator.add_profile(AgentProfile(
            name="ProductOwnerAgent", role="product_owner",
            system_prompt=(
                "Product Owner che sintetizza piani tecnici in roadmap di prodotto "
                "con priorità, metriche e rischi"
            ),
        ))
        coordinator.add_profile(AgentProfile(
            name="QAReviewerAgent", role="qa",
            system_prompt=(
                "QA Reviewer senior che valuta la qualità dei piani tecnici "
                "e delle roadmap, evidenzia rischi e propone miglioramenti concreti"
            ),
        ))
        coordinator.build_agents()

        demo_output = coordinator.run_team_demo(user_issue)
        print("\n" + demo_output + "\n")

        # Salva automaticamente il report del team in una cartella `reports/`
        reports_dir = os.path.join(os.path.dirname(__file__), "reports")
        os.makedirs(reports_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{timestamp}.txt"
        report_path = os.path.join(reports_dir, filename)

        try:
            with open(report_path, "w", encoding="utf-8") as f:
                f.write("Problema dell'utente:\n" + user_issue + "\n\n")
                f.write(demo_output)
            print(f"Report salvato in: {report_path}")
        except Exception as e:
            print(f"Impossibile salvare il report ({e}).")
    else:
        print("Usa: python run.py [--interactive | --build-agent | --build-agent-preset <preset> | --improve-agent]")
        print("  Senza argomenti: demo planner automatico")
        print("  --interactive: modalità chat interattiva")
        print("  --build-agent: crea agente custom guidato dal team")
        print("  --build-agent-preset supporto_clienti|devops_shell_sicuro|analista_requisiti|copy_marketing: crea agente preconfigurato")
        print("  --improve-agent: il team revisiona e migliora un agente esistente salvando un report in agent_reviews/\n")
        demo_planner()


if __name__ == '__main__':
    main()
