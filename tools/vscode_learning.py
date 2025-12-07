"""
VS Code Learning System - Sistema di Apprendimento per Visual Studio Code
Permette a Super Agent di apprendere dai pattern, errori, e interazioni
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import hashlib
from collections import defaultdict, Counter


class VSCodeLearningSystem:
    """Sistema di apprendimento per analizzare e migliorare l'uso di VS Code"""
    
    def __init__(self, workspace_dir: str = "."):
        """
        Inizializza il sistema di apprendimento
        
        Args:
            workspace_dir: Directory del workspace corrente
        """
        self.workspace_dir = Path(workspace_dir)
        self.learning_dir = self.workspace_dir / ".vscode" / "learning"
        self.learning_dir.mkdir(parents=True, exist_ok=True)
        
        # File di storage
        self.patterns_file = self.learning_dir / "code_patterns.json"
        self.errors_file = self.learning_dir / "error_patterns.json"
        self.commands_file = self.learning_dir / "command_history.json"
        self.snippets_file = self.learning_dir / "learned_snippets.json"
        self.preferences_file = self.learning_dir / "preferences.json"
        self.insights_file = self.learning_dir / "insights.json"
        
        # Carica dati esistenti
        self.patterns = self._load_json(self.patterns_file, {})
        self.errors = self._load_json(self.errors_file, {})
        self.commands = self._load_json(self.commands_file, [])
        self.snippets = self._load_json(self.snippets_file, {})
        self.preferences = self._load_json(self.preferences_file, {})
        self.insights = self._load_json(self.insights_file, {})
    
    def _load_json(self, file_path: Path, default: Any) -> Any:
        """Carica file JSON"""
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return default
        return default
    
    def _save_json(self, file_path: Path, data: Any):
        """Salva file JSON"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _get_code_hash(self, code: str) -> str:
        """Genera hash del codice"""
        return hashlib.md5(code.encode()).hexdigest()[:12]
    
    # ==================== APPRENDIMENTO PATTERN ====================
    
    def learn_code_pattern(
        self,
        code: str,
        pattern_type: str,
        context: Optional[str] = None,
        success: bool = True,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Apprendi un pattern di codice
        
        Args:
            code: Codice da apprendere
            pattern_type: Tipo (function, class, import, etc.)
            context: Contesto di utilizzo
            success: Se il pattern ha funzionato
            metadata: Metadati aggiuntivi
            
        Returns:
            ID del pattern appreso
        """
        pattern_id = self._get_code_hash(code)
        
        if pattern_id not in self.patterns:
            self.patterns[pattern_id] = {
                "code": code,
                "type": pattern_type,
                "context": context,
                "first_seen": datetime.now().isoformat(),
                "occurrences": 0,
                "success_count": 0,
                "failure_count": 0,
                "metadata": metadata or {}
            }
        
        # Aggiorna statistiche
        pattern = self.patterns[pattern_id]
        pattern["occurrences"] += 1
        pattern["last_seen"] = datetime.now().isoformat()
        
        if success:
            pattern["success_count"] += 1
        else:
            pattern["failure_count"] += 1
        
        # Aggiorna metadati
        if metadata:
            pattern["metadata"].update(metadata)
        
        self._save_json(self.patterns_file, self.patterns)
        return pattern_id
    
    def get_similar_patterns(
        self,
        pattern_type: str,
        min_success_rate: float = 0.8,
        limit: int = 10
    ) -> List[Dict]:
        """
        Ottieni pattern simili con alto tasso di successo
        
        Args:
            pattern_type: Tipo di pattern
            min_success_rate: Tasso minimo di successo (0-1)
            limit: Numero massimo di risultati
            
        Returns:
            Lista di pattern ordinati per successo
        """
        filtered = []
        
        for pattern_id, pattern in self.patterns.items():
            if pattern["type"] != pattern_type:
                continue
            
            total = pattern["success_count"] + pattern["failure_count"]
            if total == 0:
                continue
            
            success_rate = pattern["success_count"] / total
            if success_rate >= min_success_rate:
                filtered.append({
                    "id": pattern_id,
                    "code": pattern["code"],
                    "success_rate": success_rate,
                    "occurrences": pattern["occurrences"],
                    "context": pattern.get("context"),
                    "metadata": pattern.get("metadata", {})
                })
        
        # Ordina per success_rate e occorrenze
        filtered.sort(
            key=lambda x: (x["success_rate"], x["occurrences"]),
            reverse=True
        )
        
        return filtered[:limit]
    
    def get_pattern_recommendations(self, current_context: str) -> List[Dict]:
        """Raccomanda pattern basati sul contesto corrente"""
        recommendations = []
        
        for pattern_id, pattern in self.patterns.items():
            if not pattern.get("context"):
                continue
            
            # Similarità semplice basata su parole chiave
            context_words = set(current_context.lower().split())
            pattern_words = set(pattern["context"].lower().split())
            
            similarity = len(context_words & pattern_words) / len(context_words | pattern_words)
            
            if similarity > 0.3:  # Soglia di similarità
                total = pattern["success_count"] + pattern["failure_count"]
                success_rate = pattern["success_count"] / total if total > 0 else 0
                
                recommendations.append({
                    "id": pattern_id,
                    "code": pattern["code"],
                    "type": pattern["type"],
                    "similarity": similarity,
                    "success_rate": success_rate,
                    "occurrences": pattern["occurrences"]
                })
        
        recommendations.sort(
            key=lambda x: (x["similarity"], x["success_rate"]),
            reverse=True
        )
        
        return recommendations[:5]
    
    # ==================== APPRENDIMENTO ERRORI ====================
    
    def learn_error(
        self,
        error_type: str,
        error_message: str,
        code_context: str,
        solution: Optional[str] = None,
        file_path: Optional[str] = None
    ) -> str:
        """
        Apprendi da un errore
        
        Args:
            error_type: Tipo di errore (SyntaxError, TypeError, etc.)
            error_message: Messaggio di errore
            code_context: Codice che ha causato l'errore
            solution: Soluzione applicata
            file_path: File dove si è verificato
            
        Returns:
            ID dell'errore
        """
        error_hash = self._get_code_hash(error_message + code_context)
        
        if error_hash not in self.errors:
            self.errors[error_hash] = {
                "type": error_type,
                "message": error_message,
                "code_context": code_context,
                "file_path": file_path,
                "first_seen": datetime.now().isoformat(),
                "occurrences": 0,
                "solutions": []
            }
        
        error = self.errors[error_hash]
        error["occurrences"] += 1
        error["last_seen"] = datetime.now().isoformat()
        
        if solution and solution not in error["solutions"]:
            error["solutions"].append({
                "solution": solution,
                "applied_at": datetime.now().isoformat()
            })
        
        self._save_json(self.errors_file, self.errors)
        return error_hash
    
    def get_error_solution(self, error_type: str, error_message: str) -> Optional[str]:
        """Cerca una soluzione per un errore simile"""
        for error_hash, error in self.errors.items():
            if error["type"] == error_type and error_message in error["message"]:
                if error["solutions"]:
                    return error["solutions"][-1]["solution"]
        return None
    
    def get_common_errors(self, limit: int = 10) -> List[Dict]:
        """Ottieni gli errori più comuni"""
        errors_list = []
        
        for error_hash, error in self.errors.items():
            errors_list.append({
                "id": error_hash,
                "type": error["type"],
                "message": error["message"],
                "occurrences": error["occurrences"],
                "solutions_count": len(error["solutions"])
            })
        
        errors_list.sort(key=lambda x: x["occurrences"], reverse=True)
        return errors_list[:limit]
    
    # ==================== APPRENDIMENTO COMANDI ====================
    
    def learn_command(
        self,
        command: str,
        command_type: str,
        output: str,
        success: bool,
        execution_time: Optional[float] = None
    ):
        """
        Apprendi da un comando eseguito
        
        Args:
            command: Comando eseguito
            command_type: Tipo (terminal, vscode, python)
            output: Output del comando
            success: Se ha avuto successo
            execution_time: Tempo di esecuzione in secondi
        """
        command_entry = {
            "command": command,
            "type": command_type,
            "timestamp": datetime.now().isoformat(),
            "success": success,
            "output_length": len(output),
            "execution_time": execution_time
        }
        
        self.commands.append(command_entry)
        
        # Mantieni solo ultimi 1000 comandi
        if len(self.commands) > 1000:
            self.commands = self.commands[-1000:]
        
        self._save_json(self.commands_file, self.commands)
    
    def get_command_history(
        self,
        command_type: Optional[str] = None,
        success_only: bool = False,
        limit: int = 50
    ) -> List[Dict]:
        """Ottieni storia comandi"""
        filtered = self.commands
        
        if command_type:
            filtered = [c for c in filtered if c["type"] == command_type]
        
        if success_only:
            filtered = [c for c in filtered if c["success"]]
        
        return filtered[-limit:]
    
    def get_most_used_commands(self, limit: int = 10) -> List[Tuple[str, int]]:
        """Ottieni comandi più usati"""
        counter = Counter(cmd["command"] for cmd in self.commands)
        return counter.most_common(limit)
    
    def get_command_success_rate(self) -> Dict[str, float]:
        """Calcola tasso di successo per tipo di comando"""
        by_type = defaultdict(lambda: {"success": 0, "total": 0})
        
        for cmd in self.commands:
            cmd_type = cmd["type"]
            by_type[cmd_type]["total"] += 1
            if cmd["success"]:
                by_type[cmd_type]["success"] += 1
        
        return {
            cmd_type: stats["success"] / stats["total"] if stats["total"] > 0 else 0
            for cmd_type, stats in by_type.items()
        }
    
    # ==================== SNIPPETS APPRESI ====================
    
    def learn_snippet(
        self,
        name: str,
        code: str,
        language: str,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None
    ):
        """
        Apprendi uno snippet di codice riutilizzabile
        
        Args:
            name: Nome dello snippet
            code: Codice dello snippet
            language: Linguaggio (python, javascript, etc.)
            description: Descrizione
            tags: Tag per categorizzazione
        """
        snippet_id = f"{language}_{name.lower().replace(' ', '_')}"
        
        self.snippets[snippet_id] = {
            "name": name,
            "code": code,
            "language": language,
            "description": description or "",
            "tags": tags or [],
            "created_at": datetime.now().isoformat(),
            "used_count": self.snippets.get(snippet_id, {}).get("used_count", 0)
        }
        
        self._save_json(self.snippets_file, self.snippets)
    
    def get_snippet(self, snippet_id: str) -> Optional[Dict]:
        """Recupera uno snippet"""
        if snippet_id in self.snippets:
            self.snippets[snippet_id]["used_count"] += 1
            self._save_json(self.snippets_file, self.snippets)
            return self.snippets[snippet_id]
        return None
    
    def search_snippets(
        self,
        query: str,
        language: Optional[str] = None
    ) -> List[Dict]:
        """Cerca snippets"""
        results = []
        query_lower = query.lower()
        
        for snippet_id, snippet in self.snippets.items():
            if language and snippet["language"] != language:
                continue
            searchable = " ".join([
                snippet["name"],
                snippet["description"],
                " ".join(snippet["tags"])
            ]).lower()
            
            if query_lower in searchable:
                results.append({
                    "id": snippet_id,
                    **snippet
                })
        
        # Ordina per utilizzo
        results.sort(key=lambda x: x["used_count"], reverse=True)
        return results

    # ==================== APPRENDIMENTO CODE BASATO SU FILE ====================
    
    def learn_from_code(self, code: str, file_path: Optional[str] = None) -> str:
        """Apprendi pattern e snippet direttamente da un file"""
        context = file_path or "workspace"
        
        pattern_id = self.learn_code_pattern(
            code=code,
            pattern_type="file",
            context=context,
            success=True,
            metadata={"source": "file_analysis"}
        )
        
        snippet_id = f"learned_{self._get_code_hash(code)}"
        self.learn_snippet(
            name=snippet_id,
            code=code,
            language="python",
            description=f"Pattern appreso da {context}",
            tags=["auto", "file"]
        )
        
        return pattern_id
    
    # ==================== PREFERENZE ====================
    
    def learn_preference(self, category: str, key: str, value: Any):
        """Apprendi una preferenza dell'utente"""
        if category not in self.preferences:
            self.preferences[category] = {}
        
        self.preferences[category][key] = {
            "value": value,
            "updated_at": datetime.now().isoformat()
        }
        
        self._save_json(self.preferences_file, self.preferences)
    
    def get_preference(self, category: str, key: str, default: Any = None) -> Any:
        """Recupera una preferenza"""
        return self.preferences.get(category, {}).get(key, {}).get("value", default)
    
    def get_all_preferences(self) -> Dict:
        """Ottieni tutte le preferenze"""
        return self.preferences
    
    # ==================== INSIGHTS E ANALISI ====================
    
    def generate_insights(self) -> Dict[str, Any]:
        """Genera insights dall'apprendimento"""
        insights = {
            "generated_at": datetime.now().isoformat(),
            "summary": {},
            "recommendations": [],
            "warnings": []
        }
        
        # Statistiche pattern
        total_patterns = len(self.patterns)
        successful_patterns = sum(
            1 for p in self.patterns.values()
            if p["success_count"] > p["failure_count"]
        )
        
        insights["summary"]["patterns"] = {
            "total": total_patterns,
            "successful": successful_patterns,
            "success_rate": successful_patterns / total_patterns if total_patterns > 0 else 0
        }
        
        # Statistiche errori
        total_errors = sum(e["occurrences"] for e in self.errors.values())
        solved_errors = sum(1 for e in self.errors.values() if e["solutions"])
        
        insights["summary"]["errors"] = {
            "unique_errors": len(self.errors),
            "total_occurrences": total_errors,
            "solved": solved_errors,
            "solve_rate": solved_errors / len(self.errors) if self.errors else 0
        }
        
        # Statistiche comandi
        command_success_rate = self.get_command_success_rate()
        insights["summary"]["commands"] = {
            "total_executed": len(self.commands),
            "success_rate_by_type": command_success_rate,
            "most_used": self.get_most_used_commands(5)
        }
        
        # Raccomandazioni
        if total_patterns > 0 and successful_patterns / total_patterns < 0.7:
            insights["recommendations"].append(
                "Tasso di successo pattern basso - rivedi i pattern usati"
            )
        
        if solved_errors < len(self.errors) * 0.5:
            insights["recommendations"].append(
                "Molti errori senza soluzione - documentare soluzioni"
            )
        
        # Warnings per errori frequenti
        for error_hash, error in self.errors.items():
            if error["occurrences"] > 5 and not error["solutions"]:
                insights["warnings"].append(
                    f"Errore ricorrente senza soluzione: {error['type']} - {error['message'][:50]}"
                )
        
        # Salva insights
        self.insights = insights
        self._save_json(self.insights_file, insights)
        
        return insights
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Ottieni statistiche complete dell'apprendimento"""
        return {
            "patterns": {
                "total": len(self.patterns),
                "by_type": Counter(p["type"] for p in self.patterns.values())
            },
            "errors": {
                "total": len(self.errors),
                "by_type": Counter(e["type"] for e in self.errors.values()),
                "solved": sum(1 for e in self.errors.values() if e["solutions"])
            },
            "commands": {
                "total": len(self.commands),
                "by_type": Counter(c["type"] for c in self.commands),
                "success_rate": self.get_command_success_rate()
            },
            "snippets": {
                "total": len(self.snippets),
                "by_language": Counter(s["language"] for s in self.snippets.values()),
                "most_used": sorted(
                    self.snippets.items(),
                    key=lambda x: x[1]["used_count"],
                    reverse=True
                )[:5]
            },
            "preferences": {
                "categories": len(self.preferences),
                "total_settings": sum(len(prefs) for prefs in self.preferences.values())
            }
        }
    
    def export_knowledge_base(self, output_file: str):
        """Esporta l'intera knowledge base"""
        knowledge_base = {
            "exported_at": datetime.now().isoformat(),
            "patterns": self.patterns,
            "errors": self.errors,
            "commands": self.commands[-100:],  # Ultimi 100
            "snippets": self.snippets,
            "preferences": self.preferences,
            "insights": self.insights,
            "stats": self.get_learning_stats()
        }
        
        output_path = Path(output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(knowledge_base, f, indent=2, ensure_ascii=False)
        
        return str(output_path)
    
    def import_knowledge_base(self, input_file: str):
        """Importa knowledge base"""
        with open(input_file, 'r', encoding='utf-8') as f:
            knowledge_base = json.load(f)
        
        # Merge con dati esistenti
        self.patterns.update(knowledge_base.get("patterns", {}))
        self.errors.update(knowledge_base.get("errors", {}))
        self.snippets.update(knowledge_base.get("snippets", {}))
        self.preferences.update(knowledge_base.get("preferences", {}))
        
        # Salva tutto
        self._save_json(self.patterns_file, self.patterns)
        self._save_json(self.errors_file, self.errors)
        self._save_json(self.snippets_file, self.snippets)
        self._save_json(self.preferences_file, self.preferences)


# ==================== FUNZIONI UTILITY ====================

def quick_learn_pattern(code: str, pattern_type: str, success: bool = True):
    """Apprendi rapidamente un pattern"""
    learner = VSCodeLearningSystem()
    return learner.learn_code_pattern(code, pattern_type, success=success)


def quick_learn_error(error_type: str, error_msg: str, solution: str):
    """Apprendi rapidamente da un errore"""
    learner = VSCodeLearningSystem()
    return learner.learn_error(error_type, error_msg, "", solution)


def get_insights():
    """Ottieni insights rapidi"""
    learner = VSCodeLearningSystem()
    return learner.generate_insights()


if __name__ == "__main__":
    # Demo del sistema
    print("=" * 60)
    print("VS CODE LEARNING SYSTEM - Demo")
    print("=" * 60)
    
    learner = VSCodeLearningSystem()
    
    # Esempio 1: Apprendi pattern
    print("\n1️⃣  Apprendimento Pattern")
    pattern_id = learner.learn_code_pattern(
        code="def process_data(df):\n    return df.dropna()",
        pattern_type="function",
        context="data cleaning pandas",
        success=True,
        metadata={"framework": "pandas"}
    )
    print(f"   ✓ Pattern appreso: {pattern_id}")
    
    # Esempio 2: Apprendi errore
    print("\n2️⃣  Apprendimento Errore")
    error_id = learner.learn_error(
        error_type="AttributeError",
        error_message="'NoneType' object has no attribute 'strip'",
        code_context="text.strip()",
        solution="if text: text.strip()"
    )
    print(f"   ✓ Errore registrato: {error_id}")
    
    # Esempio 3: Apprendi comando
    print("\n3️⃣  Apprendimento Comando")
    learner.learn_command(
        command="python -m pytest tests/",
        command_type="terminal",
        output="All tests passed",
        success=True,
        execution_time=2.5
    )
    print("   ✓ Comando registrato")
    
    # Esempio 4: Apprendi snippet
    print("\n4️⃣  Apprendimento Snippet")
    learner.learn_snippet(
        name="async file reader",
        code="async with aiofiles.open(file_path) as f:\n    content = await f.read()",
        language="python",
        description="Read file asynchronously",
        tags=["async", "file", "io"]
    )
    print("   ✓ Snippet salvato")
    
    # Esempio 5: Preferenze
    print("\n5️⃣  Apprendimento Preferenze")
    learner.learn_preference("editor", "indent_size", 4)
    learner.learn_preference("terminal", "default_shell", "pwsh")
    print("   ✓ Preferenze salvate")
    
    # Genera insights
    print("\n6️⃣  Generazione Insights")
    insights = learner.generate_insights()
    print(f"   ✓ Insights generati:")
    print(f"      • Pattern: {insights['summary']['patterns']}")
    print(f"      • Errori: {insights['summary']['errors']}")
    
    # Statistiche
    print("\n7️⃣  Statistiche Apprendimento")
    stats = learner.get_learning_stats()
    print(f"   • Pattern totali: {stats['patterns']['total']}")
    print(f"   • Errori unici: {stats['errors']['total']}")
    print(f"   • Comandi eseguiti: {stats['commands']['total']}")
    print(f"   • Snippets salvati: {stats['snippets']['total']}")
    
    # Export
    print("\n8️⃣  Export Knowledge Base")
    export_path = learner.export_knowledge_base(".vscode/learning/knowledge_base.json")
    print(f"   ✓ Knowledge base esportata: {export_path}")
    
    print("\n✅ Sistema di apprendimento configurato!")
    print(f"   📁 Dati salvati in: .vscode/learning/")
