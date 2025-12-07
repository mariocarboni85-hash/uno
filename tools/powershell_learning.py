"""
PowerShell Learning System
Sistema di apprendimento per comandi, script e pattern PowerShell
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from collections import defaultdict, Counter


class PowerShellLearningSystem:
    """Sistema di apprendimento avanzato per PowerShell"""
    
    def __init__(self, learning_dir: str = "powershell_learning_data"):
        """
        Inizializza il sistema di apprendimento PowerShell
        
        Args:
            learning_dir: Directory per salvare i dati di apprendimento
        """
        self.base_dir = Path.cwd()
        self.learning_dir = self.base_dir / learning_dir
        self.learning_dir.mkdir(exist_ok=True)
        
        # Database di apprendimento
        self.commands_db = self.learning_dir / "commands.json"
        self.scripts_db = self.learning_dir / "scripts.json"
        self.patterns_db = self.learning_dir / "patterns.json"
        self.errors_db = self.learning_dir / "errors.json"
        self.aliases_db = self.learning_dir / "aliases.json"
        
        # Carica dati esistenti
        self.commands = self._load_db(self.commands_db)
        self.scripts = self._load_db(self.scripts_db)
        self.patterns = self._load_db(self.patterns_db)
        self.errors = self._load_db(self.errors_db)
        self.aliases = self._load_db(self.aliases_db)
        
        # Statistiche sessione
        self.session_stats = {
            'commands_learned': 0,
            'patterns_detected': 0,
            'errors_tracked': 0,
            'scripts_analyzed': 0
        }
        
        # Pattern PowerShell comuni
        self.powershell_patterns = {
            'cmdlet': r'\b[A-Z][a-z]+-[A-Z][a-z]+\b',
            'parameter': r'-[A-Za-z]+',
            'variable': r'\$[A-Za-z_][A-Za-z0-9_]*',
            'pipeline': r'\|',
            'foreach': r'ForEach-Object|\%',
            'where': r'Where-Object|\?',
            'select': r'Select-Object|select',
            'filter': r'-Filter|-Include|-Exclude',
            'path': r'[A-Z]:\\[\w\\.-]+',
            'script_block': r'\{[^}]+\}',
            'comment': r'#.*$',
            'here_string': r'@["\']\s*\n.*?\n["\']\@',
            'array': r'@\([^)]*\)',
            'hashtable': r'@\{[^}]*\}',
            'comparison': r'-eq|-ne|-gt|-lt|-ge|-le|-like|-notlike|-match|-notmatch',
            'logical': r'-and|-or|-not|-xor',
            'redirect': r'>|>>|2>&1',
            'splatting': r'@[A-Za-z_][A-Za-z0-9_]*',
        }
        
        # Categorie di cmdlets
        self.cmdlet_categories = {
            'Get': 'Retrieve information',
            'Set': 'Modify configuration',
            'New': 'Create new objects',
            'Remove': 'Delete objects',
            'Add': 'Add items',
            'Clear': 'Clear content',
            'Copy': 'Copy items',
            'Move': 'Move items',
            'Rename': 'Rename items',
            'Start': 'Start processes',
            'Stop': 'Stop processes',
            'Restart': 'Restart services',
            'Test': 'Test conditions',
            'Invoke': 'Execute commands',
            'Write': 'Output data',
            'Read': 'Read input',
            'Format': 'Format output',
            'Convert': 'Convert data',
            'Export': 'Export data',
            'Import': 'Import data',
            'Out': 'Output to destinations',
            'Enable': 'Enable features',
            'Disable': 'Disable features',
            'Install': 'Install components',
            'Uninstall': 'Remove components',
            'Update': 'Update components',
        }
    
    def _load_db(self, db_path: Path) -> Dict:
        """Carica database da file JSON"""
        if db_path.exists():
            try:
                with open(db_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_db(self, db_path: Path, data: Dict):
        """Salva database in file JSON"""
        with open(db_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def learn_command(self, command: str, context: str = "", success: bool = True) -> Dict[str, Any]:
        """
        Apprende da un comando PowerShell eseguito
        
        Args:
            command: Comando PowerShell
            context: Contesto di utilizzo
            success: Se il comando ha avuto successo
            
        Returns:
            Analisi del comando appreso
        """
        timestamp = datetime.now().isoformat()
        
        # Analizza il comando
        analysis = self._analyze_command(command)
        
        # Estrai cmdlet principale
        cmdlet = analysis.get('cmdlet', 'unknown')
        
        # Aggiorna database comandi
        if cmdlet not in self.commands:
            self.commands[cmdlet] = {
                'first_seen': timestamp,
                'usage_count': 0,
                'success_count': 0,
                'failure_count': 0,
                'contexts': [],
                'parameters': {},  # Dict invece di Counter
                'examples': []
            }
        
        cmd_data = self.commands[cmdlet]
        cmd_data['usage_count'] += 1
        cmd_data['last_used'] = timestamp
        
        if success:
            cmd_data['success_count'] += 1
        else:
            cmd_data['failure_count'] += 1
        
        # Aggiungi contesto se nuovo
        if context and context not in cmd_data['contexts']:
            cmd_data['contexts'].append(context)
        
        # Traccia parametri
        for param in analysis.get('parameters', []):
            if param not in cmd_data['parameters']:
                cmd_data['parameters'][param] = 0
            cmd_data['parameters'][param] += 1
        
        # Aggiungi esempio se non esiste
        if len(cmd_data['examples']) < 10:  # Max 10 esempi
            cmd_data['examples'].append({
                'command': command,
                'timestamp': timestamp,
                'success': success
            })
        
        # Salva
        self._save_db(self.commands_db, self.commands)
        self.session_stats['commands_learned'] += 1
        
        return {
            'cmdlet': cmdlet,
            'analysis': analysis,
            'learned': True,
            'usage_count': cmd_data['usage_count']
        }
    
    def _analyze_command(self, command: str) -> Dict[str, Any]:
        """Analizza un comando PowerShell"""
        analysis = {
            'command': command,
            'cmdlet': None,
            'verb': None,
            'noun': None,
            'parameters': [],
            'variables': [],
            'has_pipeline': False,
            'complexity': 0,
            'patterns': []
        }
        
        # Estrai cmdlet
        cmdlet_match = re.search(self.powershell_patterns['cmdlet'], command)
        if cmdlet_match:
            cmdlet = cmdlet_match.group()
            analysis['cmdlet'] = cmdlet
            
            # Estrai verb e noun
            if '-' in cmdlet:
                verb, noun = cmdlet.split('-', 1)
                analysis['verb'] = verb
                analysis['noun'] = noun
        
        # Estrai parametri
        params = re.findall(self.powershell_patterns['parameter'], command)
        analysis['parameters'] = list(set(params))
        
        # Estrai variabili
        vars_found = re.findall(self.powershell_patterns['variable'], command)
        analysis['variables'] = list(set(vars_found))
        
        # Rileva pipeline
        if '|' in command:
            analysis['has_pipeline'] = True
            analysis['complexity'] += 1
        
        # Rileva pattern
        for pattern_name, pattern_regex in self.powershell_patterns.items():
            if re.search(pattern_regex, command):
                analysis['patterns'].append(pattern_name)
                analysis['complexity'] += 0.5
        
        # Complessità base
        analysis['complexity'] += len(analysis['parameters']) * 0.5
        analysis['complexity'] = round(analysis['complexity'], 2)
        
        return analysis
    
    def learn_from_script(self, script_content: str, script_name: str = "unnamed") -> Dict[str, Any]:
        """
        Apprende da uno script PowerShell completo
        
        Args:
            script_content: Contenuto dello script
            script_name: Nome dello script
            
        Returns:
            Analisi dello script
        """
        timestamp = datetime.now().isoformat()
        
        # Analizza script
        lines = script_content.split('\n')
        commands = []
        cmdlets_used = Counter()
        parameters_used = Counter()
        variables_used = []
        patterns_found = Counter()
        
        for line in lines:
            line = line.strip()
            
            # Ignora commenti e righe vuote
            if not line or line.startswith('#'):
                continue
            
            # Analizza comando
            analysis = self._analyze_command(line)
            commands.append(analysis)
            
            if analysis['cmdlet']:
                cmdlets_used[analysis['cmdlet']] += 1
            
            for param in analysis['parameters']:
                parameters_used[param] += 1
            
            variables_used.extend(analysis['variables'])
            
            for pattern in analysis['patterns']:
                patterns_found[pattern] += 1
        
        # Calcola metriche
        total_lines = len(lines)
        code_lines = len([l for l in lines if l.strip() and not l.strip().startswith('#')])
        comment_lines = len([l for l in lines if l.strip().startswith('#')])
        
        script_analysis = {
            'name': script_name,
            'timestamp': timestamp,
            'metrics': {
                'total_lines': total_lines,
                'code_lines': code_lines,
                'comment_lines': comment_lines,
                'commands': len(commands),
                'unique_cmdlets': len(cmdlets_used),
                'unique_parameters': len(parameters_used),
                'unique_variables': len(set(variables_used))
            },
            'cmdlets': dict(cmdlets_used.most_common(10)),
            'parameters': dict(parameters_used.most_common(10)),
            'patterns': dict(patterns_found.most_common(10)),
            'complexity_avg': sum(c['complexity'] for c in commands) / len(commands) if commands else 0
        }
        
        # Salva nello script database
        self.scripts[script_name] = script_analysis
        self._save_db(self.scripts_db, self.scripts)
        
        # Apprendi anche i singoli comandi
        for cmd_analysis in commands:
            if cmd_analysis['cmdlet']:
                self.learn_command(cmd_analysis['command'], context=f"script:{script_name}")
        
        self.session_stats['scripts_analyzed'] += 1
        
        return script_analysis
    
    def track_error(self, command: str, error_message: str, error_type: str = "CommandError"):
        """
        Traccia un errore PowerShell per apprendimento
        
        Args:
            command: Comando che ha causato errore
            error_message: Messaggio di errore
            error_type: Tipo di errore
        """
        timestamp = datetime.now().isoformat()
        
        error_key = f"{error_type}:{command[:50]}"
        
        if error_key not in self.errors:
            self.errors[error_key] = {
                'first_seen': timestamp,
                'occurrences': 0,
                'command': command,
                'error_type': error_type,
                'messages': []
            }
        
        error_data = self.errors[error_key]
        error_data['occurrences'] += 1
        error_data['last_seen'] = timestamp
        
        if len(error_data['messages']) < 5:  # Max 5 messaggi
            error_data['messages'].append({
                'message': error_message,
                'timestamp': timestamp
            })
        
        self._save_db(self.errors_db, self.errors)
        self.session_stats['errors_tracked'] += 1
    
    def learn_alias(self, alias: str, full_command: str):
        """
        Apprende un alias PowerShell
        
        Args:
            alias: Alias breve
            full_command: Comando completo
        """
        self.aliases[alias] = {
            'full_command': full_command,
            'learned': datetime.now().isoformat()
        }
        self._save_db(self.aliases_db, self.aliases)
    
    def detect_patterns(self, command: str) -> List[Dict[str, Any]]:
        """
        Rileva pattern PowerShell in un comando
        
        Args:
            command: Comando da analizzare
            
        Returns:
            Lista di pattern rilevati
        """
        detected = []
        
        for pattern_name, pattern_regex in self.powershell_patterns.items():
            matches = re.findall(pattern_regex, command, re.MULTILINE)
            if matches:
                detected.append({
                    'pattern': pattern_name,
                    'matches': matches,
                    'count': len(matches)
                })
                
                # Traccia pattern
                pattern_key = f"{pattern_name}:frequency"
                if pattern_key not in self.patterns:
                    self.patterns[pattern_key] = {
                        'pattern': pattern_name,
                        'count': 0,
                        'examples': []
                    }
                
                self.patterns[pattern_key]['count'] += len(matches)
                
                if len(self.patterns[pattern_key]['examples']) < 5:
                    self.patterns[pattern_key]['examples'].extend(matches[:5])
        
        if detected:
            self._save_db(self.patterns_db, self.patterns)
            self.session_stats['patterns_detected'] += len(detected)
        
        return detected
    
    def get_command_suggestions(self, verb: str = None, noun: str = None) -> List[Dict[str, Any]]:
        """
        Ottiene suggerimenti di comandi in base a verb/noun
        
        Args:
            verb: Verb del cmdlet (es: Get, Set)
            noun: Noun del cmdlet (es: Process, Service)
            
        Returns:
            Lista di comandi suggeriti
        """
        suggestions = []
        
        for cmdlet, data in self.commands.items():
            if not cmdlet or '-' not in cmdlet:
                continue
            
            cmd_verb, cmd_noun = cmdlet.split('-', 1)
            
            # Filtra per verb
            if verb and cmd_verb.lower() != verb.lower():
                continue
            
            # Filtra per noun
            if noun and noun.lower() not in cmd_noun.lower():
                continue
            
            suggestions.append({
                'cmdlet': cmdlet,
                'usage_count': data['usage_count'],
                'success_rate': data['success_count'] / data['usage_count'] if data['usage_count'] > 0 else 0,
                'common_parameters': sorted(data['parameters'].items(), key=lambda x: x[1], reverse=True)[:5],
                'examples': data['examples'][:3]
            })
        
        # Ordina per usage_count
        suggestions.sort(key=lambda x: x['usage_count'], reverse=True)
        
        return suggestions
    
    def get_insights(self) -> Dict[str, Any]:
        """
        Genera insights dall'apprendimento PowerShell
        
        Returns:
            Dictionary con insights e statistiche
        """
        # Top cmdlets (filtra None)
        top_cmdlets = sorted(
            [(cmd, data['usage_count']) for cmd, data in self.commands.items() if cmd],
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        # Top verbs
        verb_usage = Counter()
        for cmdlet in self.commands.keys():
            if cmdlet and '-' in cmdlet:
                verb = cmdlet.split('-')[0]
                verb_usage[verb] += self.commands[cmdlet]['usage_count']
        
        # Errori comuni
        common_errors = sorted(
            [(err, data['occurrences']) for err, data in self.errors.items()],
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        # Pattern più usati
        top_patterns = sorted(
            [(pat, data['count']) for pat, data in self.patterns.items()],
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        # Success rate globale
        total_success = sum(data['success_count'] for data in self.commands.values())
        total_failure = sum(data['failure_count'] for data in self.commands.values())
        total_commands = total_success + total_failure
        success_rate = (total_success / total_commands * 100) if total_commands > 0 else 0
        
        return {
            'summary': {
                'total_commands_learned': len(self.commands),
                'total_scripts_analyzed': len(self.scripts),
                'total_patterns_tracked': len(self.patterns),
                'total_errors_tracked': len(self.errors),
                'total_aliases': len(self.aliases),
                'success_rate': round(success_rate, 2),
                'session_stats': self.session_stats
            },
            'top_cmdlets': [{'cmdlet': cmd, 'usage': count} for cmd, count in top_cmdlets],
            'top_verbs': [{'verb': verb, 'usage': count} for verb, count in verb_usage.most_common(10)],
            'common_errors': [{'error': err, 'occurrences': count} for err, count in common_errors],
            'top_patterns': [{'pattern': pat, 'count': count} for pat, count in top_patterns],
            'recommendations': self._generate_recommendations()
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Genera raccomandazioni basate sull'apprendimento"""
        recommendations = []
        
        # Analizza verb usage
        verb_usage = Counter()
        for cmdlet in self.commands.keys():
            if cmdlet and '-' in cmdlet:
                verb = cmdlet.split('-')[0]
                verb_usage[verb] += 1
        
        # Raccomandazioni basate su verbs
        if verb_usage.get('Get', 0) > verb_usage.get('Set', 0) * 3:
            recommendations.append("Usi molto Get-* ma poco Set-*. Considera di automatizzare anche modifiche, non solo letture.")
        
        if verb_usage.get('Start', 0) > 0 and verb_usage.get('Stop', 0) == 0:
            recommendations.append("Usi Start-* ma non Stop-*. Ricorda di fermare processi/servizi quando non servono.")
        
        # Raccomandazioni su pattern
        pipeline_usage = sum(1 for p in self.patterns.keys() if 'pipeline' in p)
        if pipeline_usage < len(self.commands) * 0.1:
            recommendations.append("Usa poco le pipeline (|). Le pipeline rendono PowerShell molto potente per combinare comandi.")
        
        # Raccomandazioni su errori
        error_rate = len(self.errors) / len(self.commands) if self.commands else 0
        if error_rate > 0.3:
            recommendations.append("Tasso di errori elevato (>30%). Controlla parametri e sintassi prima di eseguire comandi critici.")
        
        # Raccomandazioni su alias
        if len(self.aliases) < 5:
            recommendations.append("Impara alias comuni (ls → Get-ChildItem, cd → Set-Location, % → ForEach-Object) per velocizzare il lavoro.")
        
        return recommendations
    
    def export_knowledge_base(self, output_file: str = "powershell_knowledge_base.json") -> str:
        """
        Esporta tutta la knowledge base in un file
        
        Args:
            output_file: Nome file di output
            
        Returns:
            Path del file esportato
        """
        knowledge_base = {
            'exported': datetime.now().isoformat(),
            'commands': self.commands,
            'scripts': self.scripts,
            'patterns': self.patterns,
            'errors': self.errors,
            'aliases': self.aliases,
            'insights': self.get_insights()
        }
        
        output_path = self.learning_dir / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(knowledge_base, f, indent=2, ensure_ascii=False)
        
        return str(output_path)
    
    def import_knowledge_base(self, input_file: str) -> bool:
        """
        Importa knowledge base da file
        
        Args:
            input_file: Path del file da importare
            
        Returns:
            True se successo
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                knowledge_base = json.load(f)
            
            self.commands.update(knowledge_base.get('commands', {}))
            self.scripts.update(knowledge_base.get('scripts', {}))
            self.patterns.update(knowledge_base.get('patterns', {}))
            self.errors.update(knowledge_base.get('errors', {}))
            self.aliases.update(knowledge_base.get('aliases', {}))
            
            # Salva tutto
            self._save_db(self.commands_db, self.commands)
            self._save_db(self.scripts_db, self.scripts)
            self._save_db(self.patterns_db, self.patterns)
            self._save_db(self.errors_db, self.errors)
            self._save_db(self.aliases_db, self.aliases)
            
            return True
        except Exception as e:
            print(f"Errore nell'importazione: {e}")
            return False


# Utility functions

def analyze_powershell_history(history_file: str = None) -> Dict[str, Any]:
    """
    Analizza la history di PowerShell
    
    Args:
        history_file: Path al file di history (default: ConsoleHost_history.txt)
        
    Returns:
        Analisi della history
    """
    if not history_file:
        # Path default Windows
        history_file = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "PowerShell" / "PSReadLine" / "ConsoleHost_history.txt"
    
    history_file = Path(history_file)
    
    if not history_file.exists():
        return {'error': 'History file not found', 'path': str(history_file)}
    
    learner = PowerShellLearningSystem()
    
    with open(history_file, 'r', encoding='utf-8', errors='ignore') as f:
        commands = f.readlines()
    
    for cmd in commands:
        cmd = cmd.strip()
        if cmd:
            learner.learn_command(cmd, context="history")
    
    return learner.get_insights()


if __name__ == "__main__":
    # Demo
    learner = PowerShellLearningSystem()
    
    # Esempi di comandi
    test_commands = [
        "Get-Process | Where-Object {$_.CPU -gt 100} | Select-Object Name, CPU",
        "Get-ChildItem -Path C:\\Users -Recurse -Filter *.txt",
        "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser",
        "New-Item -Path .\\test -ItemType Directory",
        "Get-Service | Where-Object {$_.Status -eq 'Running'}",
        "Start-Process notepad.exe",
        "Get-Content .\\file.txt | Select-String 'pattern'",
        "Test-Path C:\\Temp",
        "Copy-Item -Path .\\source -Destination .\\dest -Recurse",
        "Get-EventLog -LogName System -Newest 10"
    ]
    
    print("🤖 PowerShell Learning System Demo\n")
    print("=" * 80)
    
    for cmd in test_commands:
        result = learner.learn_command(cmd, success=True)
        print(f"✅ Learned: {result['cmdlet']} (usage: {result['usage_count']})")
    
    print("\n" + "=" * 80)
    print("📊 INSIGHTS\n")
    
    insights = learner.get_insights()
    
    print(f"Commands learned: {insights['summary']['total_commands_learned']}")
    print(f"Success rate: {insights['summary']['success_rate']}%")
    
    print("\n🏆 Top Cmdlets:")
    for item in insights['top_cmdlets'][:5]:
        print(f"  {item['cmdlet']}: {item['usage']} uses")
    
    print("\n📝 Top Verbs:")
    for item in insights['top_verbs'][:5]:
        print(f"  {item['verb']}: {item['usage']} uses")
    
    print("\n💡 Recommendations:")
    for rec in insights['recommendations']:
        print(f"  • {rec}")
    
    print("\n" + "=" * 80)
    kb_file = learner.export_knowledge_base()
    print(f"✅ Knowledge base exported: {kb_file}")
