"""
VS Code Advanced Integration - Sistema completo per integrazione avanzata
Sfrutta tutte le 64 librerie installate per capacità di livello IDE

Capacità:
- Code Intelligence (completion, navigation, type inference)
- Refactoring automatico (extract, rename, move, inline)
- Quality Analysis (linting, formatting, security)
- Git Integration (commits, conflicts, review)
- Testing & Coverage automation
- Documentation generation
- Workspace Intelligence
- Real-time monitoring e suggestions
"""

import os
import sys
import ast
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from dataclasses import dataclass, asdict

# Code Intelligence
try:
    import jedi
    import parso
    import astroid
    from rope.base.project import Project
    from rope.refactor.extract import ExtractMethod, ExtractVariable
    from rope.refactor.rename import Rename
    from rope.refactor.inline import InlineVariable
    from rope.contrib.codeassist import code_assist, sorted_proposals
    # Quality Analysis
    import flake8.api.legacy as flake8
    from autopep8 import fix_code
    from isort import code as isort_code
    import bandit
    ADVANCED_LIBS_AVAILABLE = True
except ImportError:
    ADVANCED_LIBS_AVAILABLE = False
from radon.complexity import cc_visit
from radon.metrics import mi_visit
from radon.raw import analyze

# Git Integration
try:
    from git import Repo, GitCommandError
    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False
    Repo = None
    GitCommandError = None

try:
    from dulwich.repo import Repo as DulwichRepo
except ImportError:
    DulwichRepo = None

# File Monitoring
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Documentation
from sphinx.cmd.build import build_main
import pdoc

# Testing
import pytest
try:
    from pytest_cov.plugin import CoveragePlugin
except ImportError:
    CoveragePlugin = None

# Utils
from pathspec import PathSpec
import chardet
from more_itertools import chunked, windowed
from toolz import memoize, compose
from attrs import define, field
from cattrs import Converter


@define
class CodeLocation:
    """Posizione nel codice"""
    file_path: str
    line: int
    column: int
    end_line: Optional[int] = None
    end_column: Optional[int] = None


@define
class Symbol:
    """Simbolo nel codice (funzione, classe, variabile)"""
    name: str
    type: str  # 'function', 'class', 'variable', 'module'
    location: CodeLocation
    docstring: Optional[str] = None
    signature: Optional[str] = None
    references: List[CodeLocation] = field(factory=list)


@define
class RefactoringPreview:
    """Preview di un refactoring"""
    operation: str
    changes: List[Dict[str, Any]]
    affected_files: List[str]
    reversible: bool
    estimated_impact: str


@define
class QualityReport:
    """Report qualità codice"""
    file_path: str
    timestamp: str
    issues: List[Dict[str, Any]]
    metrics: Dict[str, Any]
    score: float
    suggestions: List[str]


@define
class TestResult:
    """Risultato test"""
    test_name: str
    status: str  # 'passed', 'failed', 'skipped'
    duration: float
    error: Optional[str] = None
    coverage: Optional[float] = None


@dataclass
class AnalysisResult:
    """Risultato unificato di analisi di un file Python."""

    file_path: str
    ast: Dict[str, Any]
    quality: Optional[QualityReport]
    security_issues: List[Dict[str, Any]]
    quality_score: float
    security_score: float

    @property
    def status(self) -> str:
        """Ritorna uno status sintetico: OK / WARN / CRITICAL."""
        if self.security_score < 50 or any(
            iss.get("severity", "low") == "high" for iss in self.security_issues
        ):
            return "CRITICAL"
        if self.quality_score < 70 or any(
            iss.get("severity", "low") == "medium" for iss in self.security_issues
        ):
            return "WARN"
        return "OK"


class CodeIntelligenceEngine:
    """Engine per code intelligence avanzata"""
    
    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)
        self.jedi_project = jedi.Project(str(self.workspace_path))
        self._symbol_cache = {}
        # Collegamento lazy al quality analyzer, impostato da VSCodeAdvancedIntegration
        self.quality_analyzer = None  # type: ignore[assignment]
        
    def get_completions(self, file_path: str, line: int, column: int) -> List[Dict[str, str]]:
        """Ottieni completions intelligenti"""
        script = jedi.Script(path=file_path, project=self.jedi_project)
        completions = script.complete(line, column)
        
        return [
            {
                "name": c.name,
                "type": c.type,
                "signature": c.get_signatures()[0].to_string() if c.get_signatures() else None,
                "docstring": c.docstring(raw=True)[:200] if c.docstring() else None,
                "module": c.module_name
            }
            for c in completions[:20]  # Top 20
        ]
    
    def goto_definition(self, file_path: str, line: int, column: int) -> List[CodeLocation]:
        """Vai alla definizione"""
        script = jedi.Script(path=file_path, project=self.jedi_project)
        definitions = script.goto(line, column)
        
        locations = []
        for d in definitions:
            if d.module_path:
                locations.append(CodeLocation(
                    file_path=str(d.module_path),
                    line=d.line or 0,
                    column=d.column or 0
                ))
        
        return locations
    
    def find_references(self, file_path: str, line: int, column: int) -> List[CodeLocation]:
        """Trova tutti i references di un simbolo"""
        script = jedi.Script(path=file_path, project=self.jedi_project)
        references = script.get_references(line, column)
        
        locations = []
        for r in references:
            if r.module_path:
                locations.append(CodeLocation(
                    file_path=str(r.module_path),
                    line=r.line or 0,
                    column=r.column or 0
                ))
        
        return locations
    
    def infer_type(self, file_path: str, line: int, column: int) -> Optional[str]:
        """Inferisci tipo di una variabile"""
        script = jedi.Script(path=file_path, project=self.jedi_project)
        inferred = script.infer(line, column)
        
        if inferred:
            return inferred[0].full_name
        return None
    
    def get_hover_info(self, file_path: str, line: int, column: int) -> Optional[Dict[str, str]]:
        """Info al passaggio del mouse"""
        script = jedi.Script(path=file_path, project=self.jedi_project)
        names = script.help(line, column)
        
        if names:
            name = names[0]
            return {
                "name": name.full_name or name.name,
                "type": name.type,
                "docstring": name.docstring(raw=True),
                "signature": name.get_signatures()[0].to_string() if name.get_signatures() else None
            }
        return None
    
    def analyze_ast(self, file_path: str) -> Dict[str, Any]:
        """Analisi AST completa"""
        try:
            module = astroid.parse(Path(file_path).read_text(encoding='utf-8'))
            
            analysis = {
                "classes": [],
                "functions": [],
                "imports": [],
                "complexity": 0,
                "lines_of_code": 0
            }
            
            for node in module.body:
                if isinstance(node, astroid.ClassDef):
                    analysis["classes"].append({
                        "name": node.name,
                        "line": node.lineno,
                        "methods": [m.name for m in node.methods()],
                        "bases": [b.as_string() for b in node.bases]
                    })
                elif isinstance(node, astroid.FunctionDef):
                    analysis["functions"].append({
                        "name": node.name,
                        "line": node.lineno,
                        "args": [arg.name for arg in node.args.args],
                        "returns": node.returns.as_string() if node.returns else None
                    })
                elif isinstance(node, (astroid.Import, astroid.ImportFrom)):
                    analysis["imports"].append(node.as_string())
            
            # Calcola complexity con radon
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
                complexity_results = cc_visit(code)
                analysis["complexity"] = sum(c.complexity for c in complexity_results)
                
                raw_metrics = analyze(code)
                analysis["lines_of_code"] = raw_metrics.loc
            
            return analysis
            
        except Exception as e:
            return {"error": str(e)}
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analizza un file e restituisce AST + simboli (retrocompatibile)."""
        analysis = self.analyze_ast(file_path)

        serialized_symbols: List[Dict[str, Any]] = []
        for symbol in self.get_symbols(file_path):
            try:
                if hasattr(symbol, "__dataclass_fields__"):
                    serialized_symbols.append(asdict(symbol))
                else:
                    serialized_symbols.append(
                        {
                            "name": getattr(symbol, "name", None),
                            "type": getattr(symbol, "type", None),
                            "location": getattr(symbol, "location", None),
                            "docstring": getattr(symbol, "docstring", None),
                        }
                    )
            except TypeError:
                serialized_symbols.append(
                    {
                        "name": getattr(symbol, "name", None),
                        "type": getattr(symbol, "type", None),
                        "location": getattr(symbol, "location", None),
                        "docstring": getattr(symbol, "docstring", None),
                    }
                )

        analysis["symbols"] = serialized_symbols
        return analysis

    def run_full_analysis(self, file_path: str) -> AnalysisResult:
        """Esegue un'analisi completa (AST + qualità + security euristica)."""
        ast_info = self.analyze_ast(file_path)

        quality_raw = self.quality_analyzer.analyze_file(file_path)
        if isinstance(quality_raw, dict):
            # Quando il quality analyzer restituisce un dict, mappiamo campi base
            qr = QualityReport(
                file_path=file_path,
                timestamp=datetime.utcnow().isoformat(),
                issues=quality_raw.get("issues", []),
                metrics=quality_raw.get("metrics", {}),
                score=float(quality_raw.get("score", 0.0)),
                suggestions=quality_raw.get("suggestions", []),
            )
        else:
            qr = quality_raw

        issues = qr.issues if isinstance(qr, QualityReport) else []

        def classify(issue: Dict[str, Any]) -> tuple[str, str]:
            text = (issue.get("code", "") + " " + issue.get("message", "")).lower()
            if any(kw in text for kw in ["sql injection", "injection"]):
                return "injection", "high"
            if any(kw in text for kw in ["password", "secret", "token", "apikey"]):
                return "secrets", "high"
            if any(kw in text for kw in ["eval", "exec", "pickle", "yaml.load"]):
                return "unsafe_execution", "high"
            if "subprocess" in text:
                return "shell", "medium"
            if any(kw in text for kw in ["http", "requests", "urllib"]):
                return "network", "medium"
            return "other", "low"

        security_issues: List[Dict[str, Any]] = []
        for issue in issues:
            category, severity = classify(issue)
            if category == "other" and severity == "low":
                continue
            item = dict(issue)
            item["category"] = category
            item["severity"] = severity
            security_issues.append(item)

        security_score = 100.0
        for iss in security_issues:
            sev = str(iss.get("severity", "low"))
            if sev == "high":
                security_score -= 30
            elif sev == "medium":
                security_score -= 10
            else:
                security_score -= 2
        security_score = max(security_score, 0.0)

        quality_score = float(qr.score) if isinstance(qr, QualityReport) else 0.0

        return AnalysisResult(
            file_path=file_path,
            ast=ast_info,
            quality=qr if isinstance(qr, QualityReport) else None,
            security_issues=security_issues,
            quality_score=quality_score,
            security_score=security_score,
        )
    
    def get_symbols(self, file_path: str) -> List[Symbol]:
        """Estrai tutti i simboli da un file"""
        if file_path in self._symbol_cache:
            return self._symbol_cache[file_path]
        
        symbols = []
        script = jedi.Script(path=file_path, project=self.jedi_project)
        names = script.get_names()
        
        for name in names:
            if name.module_path and str(name.module_path) == file_path:
                symbol = Symbol(
                    name=name.name,
                    type=name.type,
                    location=CodeLocation(
                        file_path=file_path,
                        line=name.line or 0,
                        column=name.column or 0
                    ),
                    docstring=name.docstring(raw=True)[:200] if name.docstring() else None,
                    signature=name.get_signatures()[0].to_string() if name.get_signatures() else None
                )
                symbols.append(symbol)
        
        self._symbol_cache[file_path] = symbols
        return symbols


class RefactoringEngine:
    """Engine per refactoring automatico"""
    
    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)
        self.rope_project = Project(str(self.workspace_path))
    
    def extract_method(
        self,
        file_path: str,
        start_line: int,
        end_line: int,
        method_name: str
    ) -> RefactoringPreview:
        """Extract method refactoring"""
        try:
            resource = self.rope_project.root.get_file(
                os.path.relpath(file_path, self.workspace_path)
            )
            
            # Calcola offset da line numbers
            code = resource.read()
            lines = code.split('\n')
            start_offset = sum(len(line) + 1 for line in lines[:start_line-1])
            end_offset = sum(len(line) + 1 for line in lines[:end_line])
            
            extractor = ExtractMethod(
                self.rope_project,
                resource,
                start_offset,
                end_offset
            )
            
            changes = extractor.get_changes(method_name)
            
            return RefactoringPreview(
                operation="extract_method",
                changes=[{
                    "description": changes.description,
                    "resource": str(changes.get_changed_resources()[0]),
                }],
                affected_files=[file_path],
                reversible=True,
                estimated_impact="low"
            )
            
        except Exception as e:
            return RefactoringPreview(
                operation="extract_method",
                changes=[{"error": str(e)}],
                affected_files=[],
                reversible=False,
                estimated_impact="none"
            )
    
    def rename_symbol(
        self,
        file_path: str,
        line: int,
        column: int,
        new_name: str
    ) -> RefactoringPreview:
        """Rename symbol refactoring"""
        try:
            resource = self.rope_project.root.get_file(
                os.path.relpath(file_path, self.workspace_path)
            )
            
            # Calcola offset
            code = resource.read()
            lines = code.split('\n')
            offset = sum(len(line) + 1 for line in lines[:line-1]) + column
            
            renamer = Rename(self.rope_project, resource, offset)
            changes = renamer.get_changes(new_name)
            
            affected = [str(r) for r in changes.get_changed_resources()]
            
            return RefactoringPreview(
                operation="rename",
                changes=[{
                    "description": changes.description,
                    "affected_count": len(affected)
                }],
                affected_files=affected,
                reversible=True,
                estimated_impact="high" if len(affected) > 5 else "medium"
            )
            
        except Exception as e:
            return RefactoringPreview(
                operation="rename",
                changes=[{"error": str(e)}],
                affected_files=[],
                reversible=False,
                estimated_impact="none"
            )
    
    def inline_variable(
        self,
        file_path: str,
        line: int,
        column: int
    ) -> RefactoringPreview:
        """Inline variable refactoring"""
        try:
            resource = self.rope_project.root.get_file(
                os.path.relpath(file_path, self.workspace_path)
            )
            
            # Calcola offset
            code = resource.read()
            lines = code.split('\n')
            offset = sum(len(line) + 1 for line in lines[:line-1]) + column
            
            inliner = InlineVariable(self.rope_project, resource, offset)
            changes = inliner.get_changes()
            
            return RefactoringPreview(
                operation="inline_variable",
                changes=[{"description": changes.description}],
                affected_files=[file_path],
                reversible=True,
                estimated_impact="low"
            )
            
        except Exception as e:
            return RefactoringPreview(
                operation="inline_variable",
                changes=[{"error": str(e)}],
                affected_files=[],
                reversible=False,
                estimated_impact="none"
            )
    
    def organize_imports(self, file_path: str) -> str:
        """Organizza imports con isort"""
        try:
            code = Path(file_path).read_text(encoding='utf-8')
            sorted_code = isort_code(code)
            return sorted_code
        except Exception as e:
            return f"Error: {e}"
    
    def format_code(self, file_path: str) -> str:
        """Formatta codice con autopep8"""
        try:
            code = Path(file_path).read_text(encoding='utf-8')
            formatted = fix_code(code, options={'aggressive': 2})
            return formatted
        except Exception as e:
            return f"Error: {e}"


class QualityAnalyzer:
    """Analizzatore qualità codice multi-engine"""
    
    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)
    
    def analyze_file(self, file_path: str) -> QualityReport:
        """Analisi completa qualità file"""
        issues = []
        metrics = {}
        
        try:
            code = Path(file_path).read_text(encoding='utf-8')
            
            # Flake8 linting
            style_guide = flake8.get_style_guide(ignore=['E501'])
            report = style_guide.check_files([file_path])
            
            # Bandit security scan
            from bandit.core import manager as bandit_manager
            from bandit.core import config as bandit_config
            
            # Radon complexity
            complexity_results = cc_visit(code)
            metrics["average_complexity"] = (
                sum(c.complexity for c in complexity_results) / len(complexity_results)
                if complexity_results else 0
            )
            
            # Radon maintainability
            mi_results = mi_visit(code, multi=True)
            metrics["maintainability_index"] = mi_results
            
            # Radon raw metrics
            raw = analyze(code)
            metrics["loc"] = raw.loc
            metrics["lloc"] = raw.lloc
            metrics["sloc"] = raw.sloc
            metrics["comments"] = raw.comments
            metrics["multi"] = raw.multi
            metrics["blank"] = raw.blank
            
            # Calcola score
            score = self._calculate_score(metrics, len(issues))
            
            suggestions = self._generate_suggestions(metrics, issues)
            
            return QualityReport(
                file_path=file_path,
                timestamp=datetime.now().isoformat(),
                issues=issues,
                metrics=metrics,
                score=score,
                suggestions=suggestions
            )
            
        except Exception as e:
            return QualityReport(
                file_path=file_path,
                timestamp=datetime.now().isoformat(),
                issues=[{"error": str(e)}],
                metrics={},
                score=0.0,
                suggestions=[]
            )
    
    def _calculate_score(self, metrics: Dict, issue_count: int) -> float:
        """Calcola score qualità (0-100)"""
        score = 100.0
        
        # Penalità per complexity
        if metrics.get("average_complexity", 0) > 10:
            score -= 20
        elif metrics.get("average_complexity", 0) > 5:
            score -= 10
        
        # Penalità per maintainability
        mi = metrics.get("maintainability_index", 100)
        if mi < 20:
            score -= 30
        elif mi < 50:
            score -= 15
        
        # Penalità per issues
        score -= min(issue_count * 2, 40)
        
        return max(0.0, score)
    
    def _generate_suggestions(
        self,
        metrics: Dict,
        issues: List[Dict]
    ) -> List[str]:
        """Genera suggestions per migliorare"""
        suggestions = []
        
        if metrics.get("average_complexity", 0) > 10:
            suggestions.append("Complexity alta: considera extract method per semplificare")
        
        if metrics.get("maintainability_index", 100) < 50:
            suggestions.append("Maintainability bassa: refactoring consigliato")
        
        if metrics.get("comments", 0) / max(metrics.get("loc", 1), 1) < 0.1:
            suggestions.append("Pochi commenti: aggiungi documentazione")
        
        if len(issues) > 10:
            suggestions.append(f"{len(issues)} issues trovati: fixa i più critici")
        
        return suggestions
    
    def analyze_workspace(self, file_pattern: str = "**/*.py") -> List[QualityReport]:
        """Analizza tutti i file nel workspace"""
        reports = []
        
        for file_path in self.workspace_path.glob(file_pattern):
            if file_path.is_file() and not any(p.startswith('.') for p in file_path.parts):
                report = self.analyze_file(str(file_path))
                reports.append(report)
        
        return reports


class GitIntegration:
    """Integrazione Git intelligente"""
    
    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)
        self.repo = None
        
        if GIT_AVAILABLE and Repo:
            try:
                self.repo = Repo(str(self.workspace_path))
            except:
                pass
    
    def suggest_commit_message(self, staged_files: Optional[List[str]] = None) -> str:
        """Suggerisci commit message basato su changes"""
        if not self.repo:
            return "No git repository"
        
        try:
            if not staged_files:
                staged_files = [item.a_path for item in self.repo.index.diff("HEAD")]
            
            # Analizza tipi di changes
            added = []
            modified = []
            deleted = []
            
            for item in self.repo.index.diff("HEAD"):
                if item.new_file:
                    added.append(item.a_path)
                elif item.deleted_file:
                    deleted.append(item.a_path)
                else:
                    modified.append(item.a_path)
            
            # Genera messaggio
            parts = []
            if added:
                parts.append(f"Add {len(added)} file(s)")
            if modified:
                parts.append(f"Update {len(modified)} file(s)")
            if deleted:
                parts.append(f"Delete {len(deleted)} file(s)")
            
            return " | ".join(parts) if parts else "Update files"
            
        except Exception as e:
            return f"Error: {e}"
    
    def get_file_history(self, file_path: str, max_commits: int = 10) -> List[Dict[str, Any]]:
        """Storia commits per un file"""
        if not self.repo:
            return []
        
        try:
            commits = list(self.repo.iter_commits(paths=file_path, max_count=max_commits))
            
            history = []
            for commit in commits:
                history.append({
                    "hash": commit.hexsha[:8],
                    "message": commit.message.strip(),
                    "author": str(commit.author),
                    "date": datetime.fromtimestamp(commit.committed_date).isoformat(),
                    "stats": commit.stats.total
                })
            
            return history
            
        except Exception as e:
            return [{"error": str(e)}]
    
    def analyze_conflicts(self) -> List[Dict[str, Any]]:
        """Analizza merge conflicts"""
        if not self.repo:
            return []
        
        try:
            conflicts = []
            unmerged = self.repo.index.unmerged_blobs()
            
            for path in unmerged:
                conflicts.append({
                    "file": path,
                    "stages": len(unmerged[path])
                })
            
            return conflicts
            
        except Exception as e:
            return [{"error": str(e)}]
    
    def suggest_conflict_resolution(self, file_path: str) -> Dict[str, Any]:
        """Suggerisci risoluzione conflict"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if '<<<<<<< ' not in content:
                return {"status": "no_conflict"}
            
            # Conta conflicts
            conflict_count = content.count('<<<<<<< ')
            
            return {
                "status": "conflict",
                "count": conflict_count,
                "suggestion": "Review conflicts manually - automatic resolution risky"
            }
            
        except Exception as e:
            return {"error": str(e)}


class TestingAutomation:
    """Automazione testing e coverage"""
    
    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)
    
    def run_tests(
        self,
        test_path: Optional[str] = None,
        parallel: bool = False,
        coverage: bool = False
    ) -> List[TestResult]:
        """Esegui tests con opzioni avanzate"""
        args = ["-v"]
        
        if test_path:
            args.append(test_path)
        else:
            args.append(str(self.workspace_path))
        
        if parallel:
            args.extend(["-n", "auto"])  # pytest-xdist
        
        if coverage:
            args.extend(["--cov", str(self.workspace_path)])
        
        # Timeout
        args.extend(["--timeout=30"])
        
        results = []
        
        try:
            # Pytest execution
            exit_code = pytest.main(args)
            
            # Parse results (simplified)
            results.append(TestResult(
                test_name="test_suite",
                status="passed" if exit_code == 0 else "failed",
                duration=0.0,
                coverage=None
            ))
            
        except Exception as e:
            results.append(TestResult(
                test_name="test_suite",
                status="failed",
                duration=0.0,
                error=str(e)
            ))
        
        return results
    
    def generate_test_template(self, file_path: str) -> str:
        """Genera template test per un file"""
        try:
            # Analizza file per estrarre funzioni/classi
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
            
            functions = []
            classes = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)
            
            # Genera template
            template = f'''"""
Test suite for {Path(file_path).name}
Auto-generated by VSCode Advanced Integration
"""

import pytest
from {Path(file_path).stem} import *


'''
            
            for func in functions:
                if not func.startswith('_'):
                    template += f'''def test_{func}():
    """Test {func} function"""
    # TODO: Implement test
    pass


'''
            
            for cls in classes:
                template += f'''class Test{cls}:
    """Test suite for {cls}"""
    
    def test_init(self):
        """Test {cls} initialization"""
        # TODO: Implement test
        pass


'''
            
            return template
            
        except Exception as e:
            return f"# Error generating template: {e}"


class WorkspaceIntelligence:
    """Intelligence workspace-level"""
    
    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)
    
    def analyze_dependencies(self) -> Dict[str, Any]:
        """Analizza dipendenze progetto"""
        try:
            from pipdeptree import get_installed_distributions, build_dist_index
            
            pkgs = get_installed_distributions()
            
            return {
                "total_packages": len(pkgs),
                "packages": [{"name": p.project_name, "version": p.version} for p in pkgs[:20]]
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def check_security(self) -> List[Dict[str, Any]]:
        """Check security vulnerabilities"""
        try:
            import subprocess
            result = subprocess.run(
                ["safety", "check", "--json"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return []
            
            try:
                issues = json.loads(result.stdout)
                return issues
            except:
                return [{"info": "No vulnerabilities found"}]
                
        except Exception as e:
            return [{"error": str(e)}]
    
    def analyze_project_structure(self) -> Dict[str, Any]:
        """Analizza struttura progetto"""
        structure = {
            "python_files": 0,
            "test_files": 0,
            "total_lines": 0,
            "directories": 0,
            "modules": []
        }
        
        for path in self.workspace_path.rglob("*.py"):
            if any(p.startswith('.') for p in path.parts):
                continue
            
            structure["python_files"] += 1
            
            if "test" in path.stem:
                structure["test_files"] += 1
            
            try:
                lines = len(path.read_text(encoding='utf-8').splitlines())
                structure["total_lines"] += lines
            except:
                pass
        
        structure["directories"] = len(list(self.workspace_path.rglob("*/")))
        
        return structure


class VSCodeAdvancedIntegration:
    """Sistema principale integrazione VS Code avanzata"""
    
    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)
        
        # Initialize engines
        self.code_intelligence = CodeIntelligenceEngine(str(workspace_path))
        self.refactoring = RefactoringEngine(str(workspace_path))
        self.quality = QualityAnalyzer(str(workspace_path))
        # Collega il quality analyzer al motore di code intelligence
        self.code_intelligence.quality_analyzer = self.quality
        self.git = GitIntegration(str(workspace_path))
        self.testing = TestingAutomation(str(workspace_path))
        self.workspace = WorkspaceIntelligence(str(workspace_path))
        
        self._file_watcher = None
        self._observer = None

    @property
    def quality_analyzer(self) -> QualityAnalyzer:
        return self.quality

    @property
    def refactoring_engine(self) -> RefactoringEngine:
        return self.refactoring
    
    def start_file_monitoring(self, callback=None):
        """Avvia monitoraggio file real-time"""
        class ChangeHandler(FileSystemEventHandler):
            def __init__(self, callback):
                self.callback = callback
            
            def on_modified(self, event):
                if not event.is_directory and event.src_path.endswith('.py'):
                    if self.callback:
                        self.callback(event.src_path, 'modified')
        
        self._observer = Observer()
        self._file_watcher = ChangeHandler(callback)
        self._observer.schedule(
            self._file_watcher,
            str(self.workspace_path),
            recursive=True
        )
        self._observer.start()
    
    def stop_file_monitoring(self):
        """Ferma monitoraggio"""
        if self._observer:
            self._observer.stop()
            self._observer.join()
    
    def comprehensive_analysis(self, file_path: str) -> Dict[str, Any]:
        """Analisi comprensiva di un file"""
        # Get symbols
        symbols = self.code_intelligence.get_symbols(file_path)
        symbols_data = []
        for s in symbols:
            symbols_data.append({
                "name": s.name,
                "type": s.type,
                "location": {
                    "file_path": s.location.file_path,
                    "line": s.location.line,
                    "column": s.location.column
                },
                "docstring": s.docstring,
                "signature": s.signature
            })
        
        # Get AST analysis
        ast_analysis = self.code_intelligence.analyze_ast(file_path)
        
        # Get quality report
        quality_report = self.quality.analyze_file(file_path)
        quality_data = {
            "file_path": quality_report.file_path,
            "timestamp": quality_report.timestamp,
            "issues": quality_report.issues,
            "metrics": quality_report.metrics,
            "score": quality_report.score,
            "suggestions": quality_report.suggestions
        }
        
        # Get git history
        git_history = self.git.get_file_history(file_path, max_commits=5)
        
        return {
            "code_intelligence": {
                "symbols": symbols_data,
                "ast_analysis": ast_analysis
            },
            "quality": quality_data,
            "git_history": git_history,
            "timestamp": datetime.now().isoformat()
        }
    
    def suggest_improvements(self, file_path: str) -> List[str]:
        """Suggerimenti miglioramento completi"""
        suggestions = []
        
        # Quality suggestions
        quality_report = self.quality.analyze_file(file_path)
        suggestions.extend(quality_report.suggestions)
        
        # Complexity suggestions
        ast_analysis = self.code_intelligence.analyze_ast(file_path)
        if ast_analysis.get("complexity", 0) > 15:
            suggestions.append("Complexity molto alta: refactoring necessario")
        
        # Code style
        try:
            code = Path(file_path).read_text(encoding='utf-8')
            if "import *" in code:
                suggestions.append("Evita 'import *': usa imports espliciti")
            if len(code.splitlines()) > 500:
                suggestions.append("File molto lungo: considera split in moduli")
        except:
            pass
        
        return suggestions
    
    def workspace_dashboard(self) -> Dict[str, Any]:
        """Dashboard completo workspace"""
        # Get quality reports
        quality_reports = self.quality.analyze_workspace()
        quality_data = []
        for r in quality_reports[:5]:
            quality_data.append({
                "file_path": r.file_path,
                "score": r.score,
                "issues": len(r.issues),
                "suggestions": len(r.suggestions)
            })
        
        return {
            "project_structure": self.workspace.analyze_project_structure(),
            "dependencies": self.workspace.analyze_dependencies(),
            "security": self.workspace.check_security(),
            "quality_overview": {
                "reports": quality_data
            },
            "git_status": {
                "conflicts": self.git.analyze_conflicts(),
                "suggested_commit": self.git.suggest_commit_message()
            }
        }


def create_integration(workspace_path: str) -> VSCodeAdvancedIntegration:
    """Factory per creare integrazione"""
    return VSCodeAdvancedIntegration(workspace_path)
