"""Team coordination for multiple SuperAgents working together.

This module defines AgentProfile and TeamCoordinator, which manage
multiple specialized SuperAgent instances collaborating on tasks
like building custom agents.
"""
from dataclasses import dataclass
from typing import Dict, List, Optional, Callable

from agent import SuperAgent


@dataclass
class AgentProfile:
    """Configuration for a specialized agent in the team."""

    name: str
    role: str
    system_prompt: str


class TeamCoordinator:
    """Coordinates a group of specialized SuperAgents.

    This is a first simple version that chains calls between agents.
    """

    def __init__(self, base_tools: Dict[str, Callable]):
        self.base_tools = base_tools
        self.profiles: List[AgentProfile] = []
        self.agents: Dict[str, SuperAgent] = {}

    def add_profile(self, profile: AgentProfile):
        """Register a new specialized agent profile."""
        self.profiles.append(profile)

    def build_agents(self):
        """Instantiate SuperAgent objects for all profiles.

        For now, we just pass the same tools. Specialization is logical
        (via role / prompts) and can be extended later.
        """
        for profile in self.profiles:
            # Name encodes role for traceability
            agent = SuperAgent(self.base_tools, name=profile.name)
            self.agents[profile.role] = agent

    def get_agent(self, role: str) -> Optional[SuperAgent]:
        return self.agents.get(role)

    def describe_team(self) -> str:
        lines = ["Team di super agenti:"]
        for p in self.profiles:
            lines.append(f"- {p.name} ({p.role})")
        return "\n".join(lines)

    def run_team_demo(self, user_issue: str) -> str:
        """Demo semplice: fa collaborare più agenti su uno stesso task.

        - L'agente di ruolo "requirements" prova a chiarire il problema.
        - L'agente di ruolo "design" propone un piano di azione.
        - (Opzionale) l'agente di ruolo "product_owner" sintetizza
          un piano di rilascio / roadmap a partire dagli step.
        Il risultato è restituito come testo unico.
        """
        if not self.agents:
            self.build_agents()

        req_agent = self.get_agent("requirements")
        des_agent = self.get_agent("design")
        po_agent = self.get_agent("product_owner")
        qa_agent = self.get_agent("qa")

        parts = ["=== Team Demo ===", f"Input utente: {user_issue}"]

        if req_agent:
            # In contesti senza LLM funzionante, potresti voler sostituire
            # queste chiamate con una logica mock. Qui restiamo semplici.
            clarified = req_agent.ask(
                "Analizza e chiarisci questo problema dell'utente, "
                "proponendo domande di chiarimento se necessario:\n" + user_issue
            )
            parts.append("\n[Analista Requisiti]\n" + str(clarified))
        else:
            parts.append("\n[Analista Requisiti]\n(nessun agente configurato)")

        if des_agent:
            designed = des_agent.ask(
                "Dato questo problema chiarito, proponi un piano di azione "
                "in 3-5 passi:\n" + user_issue
            )
            parts.append("\n[Architetto/Designer]\n" + str(designed))
        else:
            parts.append("\n[Architetto/Designer]\n(nessun agente configurato)")

        # Product Owner / Stratega: sintetizza in termini di roadmap e valore
        if po_agent:
            design_text = str(designed) if des_agent else user_issue
            po_summary = po_agent.ask(
                "Sei un Product Owner. Prendi questo piano tecnico e "
                "trasformalo in una roadmap di prodotto con priorità, "
                "metriche di successo e rischi principali:\n" + design_text
            )
            parts.append("\n[Product Owner]\n" + str(po_summary))
        else:
            parts.append("\n[Product Owner]\n(nessun agente configurato)")

        # QA Reviewer: valuta la qualità e la robustezza del piano
        if qa_agent:
            full_context_for_qa = "".join([
                "Problema utente:\n",
                user_issue,
                "\n\n",
                "Sezione Analista Requisiti:\n",
                str(clarified) if req_agent else "(nessun contenuto)",
                "\n\n",
                "Sezione Architetto/Designer:\n",
                str(designed) if des_agent else "(nessun contenuto)",
                "\n\n",
                "Sezione Product Owner / Roadmap:\n",
                str(po_summary) if po_agent else "(nessun contenuto)",
            ])

            qa_feedback = qa_agent.ask(
                "Sei un QA Reviewer senior. Ti fornisco:\n"
                "- il problema originale dell'utente,\n"
                "- l'analisi requisiti,\n"
                "- il piano di design,\n"
                "- la roadmap di prodotto.\n\n"
                "Devi:\n"
                "1) Evidenziare criticità, ambiguità o rischi non coperti.\n"
                "2) Segnalare ipotesi nascoste o troppo ottimistiche.\n"
                "3) Proporre miglioramenti concreti al piano e alla roadmap.\n"
                "4) Indicare eventuali test, metriche o esperimenti da fare.\n\n"
                "Rispondi in forma di checklist puntata, molto pratica e concreta.\n\n"
                + full_context_for_qa
            )

            parts.append("\n[QA Reviewer]\n" + str(qa_feedback))
        else:
            parts.append("\n[QA Reviewer]\n(nessun agente configurato)")

        return "\n".join(parts)

    def run_team_structured(self, user_issue: str) -> Dict[str, str]:
        """Versione strutturata della demo team.

        Ritorna un dict con chiavi:
        - "requirements"
        - "design"
        - "roadmap"
        - "qa_feedback"
        - "full_report" (testo completo come run_team_demo)
        """
        if not self.agents:
            self.build_agents()

        req_agent = self.get_agent("requirements")
        des_agent = self.get_agent("design")
        po_agent = self.get_agent("product_owner")
        qa_agent = self.get_agent("qa")

        artifacts: Dict[str, str] = {
            "requirements": "",
            "design": "",
            "roadmap": "",
            "qa_feedback": "",
        }

        parts = ["=== Team Demo ===", f"Input utente: {user_issue}"]

        if req_agent:
            clarified = req_agent.ask(
                "Analizza e chiarisci questo problema dell'utente, "
                "proponendo domande di chiarimento se necessario:\n" + user_issue
            )
            clarified_str = str(clarified)
            artifacts["requirements"] = clarified_str
            parts.append("\n[Analista Requisiti]\n" + clarified_str)
        else:
            parts.append("\n[Analista Requisiti]\n(nessun agente configurato)")

        if des_agent:
            designed = des_agent.ask(
                "Dato questo problema chiarito, proponi un piano di azione "
                "in 3-5 passi:\n" + (artifacts["requirements"] or user_issue)
            )
            designed_str = str(designed)
            artifacts["design"] = designed_str
            parts.append("\n[Architetto/Designer]\n" + designed_str)
        else:
            parts.append("\n[Architetto/Designer]\n(nessun agente configurato)")

        if po_agent:
            design_text = artifacts["design"] or user_issue
            po_summary = po_agent.ask(
                "Sei un Product Owner. Prendi questo piano tecnico e "
                "trasformalo in una roadmap di prodotto con priorità, "
                "metriche di successo e rischi principali:\n" + design_text
            )
            po_str = str(po_summary)
            artifacts["roadmap"] = po_str
            parts.append("\n[Product Owner]\n" + po_str)
        else:
            parts.append("\n[Product Owner]\n(nessun agente configurato)")

        if qa_agent:
            full_context_for_qa = "".join([
                "Problema utente:\n",
                user_issue,
                "\n\n",
                "Sezione Analista Requisiti:\n",
                artifacts["requirements"] or "(nessun contenuto)",
                "\n\n",
                "Sezione Architetto/Designer:\n",
                artifacts["design"] or "(nessun contenuto)",
                "\n\n",
                "Sezione Product Owner / Roadmap:\n",
                artifacts["roadmap"] or "(nessun contenuto)",
            ])

            qa_feedback = qa_agent.ask(
                "Sei un QA Reviewer senior. Ti fornisco:\n"
                "- il problema originale dell'utente,\n"
                "- l'analisi requisiti,\n"
                "- il piano di design,\n"
                "- la roadmap di prodotto.\n\n"
                "Devi:\n"
                "1) Evidenziare criticità, ambiguità o rischi non coperti.\n"
                "2) Segnalare ipotesi nascoste o troppo ottimistiche.\n"
                "3) Proporre miglioramenti concreti al piano e alla roadmap.\n"
                "4) Indicare eventuali test, metriche o esperimenti da fare.\n\n"
                "Rispondi in forma di checklist puntata, molto pratica e concreta.\n\n"
                + full_context_for_qa
            )

            qa_str = str(qa_feedback)
            artifacts["qa_feedback"] = qa_str
            parts.append("\n[QA Reviewer]\n" + qa_str)
        else:
            parts.append("\n[QA Reviewer]\n(nessun agente configurato)")

        artifacts["full_report"] = "\n".join(parts)
        return artifacts

    def run_build_flow(self, specification: str) -> Dict[str, str]:
        """High-level cooperative flow to design a custom agent.

        Returns a dict with intermediate artifacts (requirements, design, files_plan).
        """
        from tools.llm import think  # reuse shared LLM helper

        if not self.agents:
            self.build_agents()

        artifacts: Dict[str, str] = {}

        # 1) Requirements
        req_agent = self.get_agent("requirements")
        if req_agent is None:
            # fallback: use LLM directly
            requirements_prompt = (
                "Sei un analista requisiti. Dato questo bisogno utente, "
                "produci requisiti strutturati per un agente software custom.\n\n" + specification
            )
            artifacts["requirements"] = think(requirements_prompt)
        else:
            requirements_prompt = (
                "Analizza questo bisogno utente e produci requisiti strutturati "
                "per un agente software custom.\n\n" + specification
            )
            # req_agent.ask dovrebbe restituire str; cast difensivo
            artifacts["requirements"] = str(req_agent.ask(requirements_prompt))

        # 2) Design
        design_agent = self.get_agent("design")
        requirements_text = str(artifacts.get("requirements", ""))
        design_prompt = (
            "Sei un architetto software di agenti. Dati questi requisiti, "
            "progetta la struttura di un agente (moduli, tools, flusso).\n\n" + requirements_text
        )
        if design_agent is None:
            artifacts["design"] = think(design_prompt)
        else:
            artifacts["design"] = str(design_agent.ask(design_prompt))

        # 3) Implementation plan (file plan)
        impl_agent = self.get_agent("implementation")
        design_text = str(artifacts.get("design", ""))
        impl_prompt = (
            "Sei uno sviluppatore Python. In base a questo design, "
            "elenca in formato chiaro i file da creare (percorsi) e il loro scopo.\n\n" + design_text
        )
        if impl_agent is None:
            artifacts["files_plan"] = think(impl_prompt)
        else:
            artifacts["files_plan"] = str(impl_agent.ask(impl_prompt))

        return artifacts

    def review_existing_agent(self, agent_description: str) -> Dict[str, str]:
        """Analizza e suggerisce miglioramenti per un agente esistente.

        L'input è una descrizione libera dell'agente: obiettivi, prompt attuale,
        strumenti disponibili, problemi riscontrati.

        Ritorna un dict con:
        - "issues": problemi e limiti individuati
        - "improvements": suggerimenti concreti di miglioramento
        - "risks": rischi e failure mode
        - "qa_feedback": revisione QA strutturata
        """
        if not self.agents:
            self.build_agents()

        req_agent = self.get_agent("requirements")
        des_agent = self.get_agent("design")
        qa_agent = self.get_agent("qa")

        from tools.llm import think

        result: Dict[str, str] = {
            "issues": "",
            "improvements": "",
            "risks": "",
            "qa_feedback": "",
        }

        # 1) Requirements: capire davvero cosa fa oggi l'agente e cosa dovrebbe fare
        if req_agent:
            issues_text = req_agent.ask(
                "Sei un analista. Ti descrivo un agente AI esistente (scopo, prompt, "
                "strumenti, problemi). Estrai e riassumi:\n"
                "- problemi principali,\n"
                "- lacune nei requisiti,\n"
                "- casi d'uso mancanti,\n"
                "- vincoli impliciti.\n\n" + agent_description
            )
            result["issues"] = str(issues_text)
        else:
            result["issues"] = think(
                "Analizza questo agente descritto in testo libero e riassumi "
                "problemi, lacune e casi d'uso mancanti:\n\n" + agent_description
            )

        # 2) Design: suggerire modifiche strutturali (prompt, tools, flusso)
        design_input = agent_description + "\n\nProblemi identificati:\n" + result["issues"]
        if des_agent:
            improvements_text = des_agent.ask(
                "Sei un architetto di agenti AI. In base alla descrizione "
                "dell'agente e ai problemi emersi, proponi miglioramenti concreti a:\n"
                "- prompt di sistema e istruzioni operative,\n"
                "- scelta e uso dei tools,\n"
                "- flusso di ragionamento (passi),\n"
                "- gestione errori e limiti.\n\n" + design_input
            )
            result["improvements"] = str(improvements_text)
        else:
            result["improvements"] = think(
                "Proponi miglioramenti strutturali per questo agente (prompt, tools, "
                "flusso, gestione errori):\n\n" + design_input
            )

        # 3) Rischi / failure mode
        risks_prompt = (
            "Sei un esperto di affidabilità AI. Dato questo agente e i problemi "
            "identificati, elenca i principali rischi, failure mode, casi in cui "
            "potrebbe fare danni o dare risposte fuorvianti, e come mitigarli.\n\n"
            + design_input
        )
        result["risks"] = think(risks_prompt)

        # 4) QA reviewer: checklist finale
        if qa_agent:
            qa_feedback = qa_agent.ask(
                "Sei un QA Reviewer senior per agenti AI. Ti fornisco:\n"
                "- descrizione dell'agente,\n"
                "- problemi attuali,\n"
                "- proposte di miglioramento.\n\n"
                "Scrivi una checklist pratica di verifica e miglioramento, con punti:\n"
                "[OK] / [DA MIGLIORARE] e azioni concrete.\n\n"
                + "Descrizione agente:\n" + agent_description
                + "\n\nProblemi:\n" + result["issues"]
                + "\n\nMiglioramenti proposti:\n" + result["improvements"]
            )
            result["qa_feedback"] = str(qa_feedback)
        else:
            result["qa_feedback"] = think(
                "Agisci come QA Reviewer e produci una checklist di miglioramento "
                "per questo agente AI:\n\n" + agent_description
            )

        return result
