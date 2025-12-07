"""
Documentation Generator - Generazione automatica documentazione
Usa sphinx, mkdocs, pdoc per generare docs da codice
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
import ast
import inspect
import json
from datetime import datetime

# Documentation tools
import pdoc
from sphinx.application import Sphinx
from sphinx.util.console import color_terminal


class DocumentationGenerator:
    """Generatore documentazione automatica"""
    
    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)
        self.docs_path = self.workspace_path / "docs"
        self.docs_path.mkdir(exist_ok=True)
    
    def extract_docstrings(self, file_path: str) -> Dict[str, Any]:
        """Estrai tutti i docstrings da un file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
            
            docstrings = {
                "module": ast.get_docstring(tree),
                "functions": {},
                "classes": {}
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    doc = ast.get_docstring(node)
                    if doc:
                        docstrings["functions"][node.name] = {
                            "docstring": doc,
                            "line": node.lineno,
                            "args": [arg.arg for arg in node.args.args]
                        }
                
                elif isinstance(node, ast.ClassDef):
                    doc = ast.get_docstring(node)
                    methods = {}
                    
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            method_doc = ast.get_docstring(item)
                            if method_doc:
                                methods[item.name] = method_doc
                    
                    docstrings["classes"][node.name] = {
                        "docstring": doc,
                        "line": node.lineno,
                        "methods": methods
                    }
            
            return docstrings
            
        except Exception as e:
            return {"error": str(e)}
    
    def generate_markdown_docs(self, file_path: str) -> str:
        """Genera documentazione markdown da file Python"""
        docstrings = self.extract_docstrings(file_path)
        
        if "error" in docstrings:
            return f"# Error\n\n{docstrings['error']}"
        
        filename = Path(file_path).name
        md = f"# {filename}\n\n"
        
        if docstrings["module"]:
            md += f"{docstrings['module']}\n\n"
        
        # Functions
        if docstrings["functions"]:
            md += "## Functions\n\n"
            for name, info in docstrings["functions"].items():
                args_str = ", ".join(info["args"])
                md += f"### `{name}({args_str})`\n\n"
                md += f"{info['docstring']}\n\n"
                md += f"*Line {info['line']}*\n\n"
        
        # Classes
        if docstrings["classes"]:
            md += "## Classes\n\n"
            for name, info in docstrings["classes"].items():
                md += f"### `class {name}`\n\n"
                if info["docstring"]:
                    md += f"{info['docstring']}\n\n"
                
                if info["methods"]:
                    md += "**Methods:**\n\n"
                    for method_name, method_doc in info["methods"].items():
                        md += f"- **`{method_name}()`**: {method_doc.split(chr(10))[0]}\n"
                    md += "\n"
                
                md += f"*Line {info['line']}*\n\n"
        
        return md
    
    def generate_api_reference(self, module_name: str) -> str:
        """Genera API reference con pdoc"""
        try:
            import importlib
            module = importlib.import_module(module_name)
            
            # Usa pdoc per generare HTML
            doc_html = pdoc.html(module_name, docfilter=None)
            
            # Salva
            output_file = self.docs_path / f"{module_name}_api.html"
            output_file.write_text(doc_html, encoding='utf-8')
            
            return f"API reference generated: {output_file}"
            
        except Exception as e:
            return f"Error: {e}"
    
    def generate_project_readme(self, analysis: Dict[str, Any]) -> str:
        """Genera README.md per progetto"""
        readme = f"""# Project Documentation

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Project Structure

- **Python Files**: {analysis.get('python_files', 0)}
- **Test Files**: {analysis.get('test_files', 0)}
- **Total Lines**: {analysis.get('total_lines', 0)}
- **Directories**: {analysis.get('directories', 0)}

## Modules

"""
        
        for module in analysis.get('modules', [])[:10]:
            readme += f"- `{module}`\n"
        
        readme += """

## Installation

```bash
pip install -r requirements.txt
```

## Usage

[Add usage examples here]

## Testing

```bash
pytest tests/
```

## Contributing

[Add contribution guidelines]

## License

[Add license information]
"""
        
        return readme
    
    def create_changelog(self, git_history: List[Dict]) -> str:
        """Genera CHANGELOG.md da git history"""
        changelog = "# Changelog\n\n"
        changelog += "All notable changes to this project.\n\n"
        
        current_date = None
        
        for commit in git_history:
            commit_date = commit.get('date', '').split('T')[0]
            
            if commit_date != current_date:
                changelog += f"\n## {commit_date}\n\n"
                current_date = commit_date
            
            changelog += f"- {commit.get('message', '')} ({commit.get('hash', '')})\n"
        
        return changelog
    
    def generate_type_stubs(self, file_path: str) -> str:
        """Genera .pyi stub file con type hints"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
            
            stub = '"""Type stubs for {filename}"""\n\n'.format(
                filename=Path(file_path).name
            )
            
            # Imports
            stub += "from typing import Any, Optional, List, Dict, Tuple\n\n"
            
            # Functions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    args = ", ".join(
                        f"{arg.arg}: Any" for arg in node.args.args
                    )
                    stub += f"def {node.name}({args}) -> Any: ...\n\n"
                
                elif isinstance(node, ast.ClassDef):
                    stub += f"class {node.name}:\n"
                    
                    has_methods = False
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            has_methods = True
                            args = ", ".join(
                                f"{arg.arg}: Any" for arg in item.args.args
                            )
                            stub += f"    def {item.name}({args}) -> Any: ...\n"
                    
                    if not has_methods:
                        stub += "    pass\n"
                    
                    stub += "\n"
            
            return stub
            
        except Exception as e:
            return f"# Error: {e}"
    
    def generate_module_index(self, base_path: Optional[str] = None) -> str:
        """Genera indice di tutti i moduli"""
        if base_path is None:
            base_path = self.workspace_path
        else:
            base_path = Path(base_path)
        
        index = "# Module Index\n\n"
        
        modules = []
        for py_file in base_path.rglob("*.py"):
            if any(p.startswith('.') for p in py_file.parts):
                continue
            if py_file.stem == "__init__":
                continue
            
            relative = py_file.relative_to(base_path)
            module_path = str(relative.with_suffix('')).replace(os.sep, '.')
            
            # Estrai module docstring
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read())
                    doc = ast.get_docstring(tree)
                    
                modules.append({
                    "path": module_path,
                    "file": str(relative),
                    "docstring": doc.split('\n')[0] if doc else "No description"
                })
            except:
                pass
        
        for module in sorted(modules, key=lambda x: x['path']):
            index += f"## `{module['path']}`\n\n"
            index += f"{module['docstring']}\n\n"
            index += f"*File: {module['file']}*\n\n"
        
        return index
    
    def generate_full_documentation(self) -> Dict[str, str]:
        """Genera documentazione completa per workspace"""
        results = {}
        
        # Module index
        index_file = self.docs_path / "INDEX.md"
        index_content = self.generate_module_index()
        index_file.write_text(index_content, encoding='utf-8')
        results["index"] = str(index_file)
        
        # Per ogni file Python
        for py_file in self.workspace_path.rglob("*.py"):
            if any(p.startswith('.') for p in py_file.parts):
                continue
            
            # Markdown docs
            doc_file = self.docs_path / f"{py_file.stem}_docs.md"
            doc_content = self.generate_markdown_docs(str(py_file))
            doc_file.write_text(doc_content, encoding='utf-8')
            
            # Type stubs
            stub_file = self.docs_path / f"{py_file.stem}.pyi"
            stub_content = self.generate_type_stubs(str(py_file))
            stub_file.write_text(stub_content, encoding='utf-8')
            
            results[py_file.stem] = f"docs: {doc_file}, stub: {stub_file}"
        
        return results


# Aggiungi al VSCodeAdvancedIntegration
def add_documentation_to_integration():
    """Extend VSCodeAdvancedIntegration con DocumentationGenerator"""
    import tools.vscode_advanced_integration as vai
    
    original_init = vai.VSCodeAdvancedIntegration.__init__
    
    def new_init(self, workspace_path: str):
        original_init(self, workspace_path)
        self.documentation = DocumentationGenerator(str(workspace_path))
    
    vai.VSCodeAdvancedIntegration.__init__ = new_init
