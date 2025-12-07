def analyze_code(params):
    """
    Analisi statica del codice (mock).
    params: {'path': ...}
    """
    path = params.get('path')
    # Mock: restituisce conteggio righe
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return {'lines': len(lines)}
    except Exception as e:
        return {'error': str(e)}
def generate_docs(params):
    """
    Genera documentazione automatica (mock).
    params: {'source': ..., 'dest': ...}
    """
    source = params.get('source')
    dest = params.get('dest')
    # Mock: copia il file sorgente come documentazione
    import shutil
    try:
        shutil.copy(source, dest)
        return {'result': 'ok'}
    except Exception as e:
        return {'error': str(e)}
def compress_files(params):
    """
    Comprimi file/cartelle in ZIP.
    params: {'paths': [...], 'zip_path': ...}
    """
    import zipfile
    zip_path = params.get('zip_path')
    paths = params.get('paths', [])
    try:
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for p in paths:
                zipf.write(p)
        return {'result': 'ok'}
    except Exception as e:
        return {'error': str(e)}
def monitor_directory(params):
    """
    Monitora una directory per modifiche (mock).
    params: {'path': ...}
    """
    path = params.get('path')
    # Mock: restituisce lista file attuale
    import os
    try:
        return {'files': os.listdir(path)}
    except Exception as e:
        return {'error': str(e)}
def create_project_template(params):
    """
    Genera un template di progetto.
    params: {'type': 'python'|'node', 'path': ...}
    """
    import os
    t = params.get('type')
    path = params.get('path')
    try:
        os.makedirs(path, exist_ok=True)
        if t == 'python':
            with open(os.path.join(path, 'main.py'), 'w') as f:
                f.write('print("Hello from Python project!")\n')
            with open(os.path.join(path, 'requirements.txt'), 'w') as f:
                f.write('')
        elif t == 'node':
            with open(os.path.join(path, 'index.js'), 'w') as f:
                f.write('console.log("Hello from Node project!");\n')
            with open(os.path.join(path, 'package.json'), 'w') as f:
                f.write('{\n  "name": "node-project"\n}\n')
        else:
            return {'error': 'Tipo non supportato'}
        return {'result': 'ok'}
    except Exception as e:
        return {'error': str(e)}
def download_file(params):
    """
    Scarica un file da internet.
    params: {'url': ..., 'dest': ...}
    """
    import requests
    url = params.get('url')
    dest = params.get('dest')
    try:
        r = requests.get(url)
        with open(dest, 'wb') as f:
            f.write(r.content)
        return {'result': 'ok'}
    except Exception as e:
        return {'error': str(e)}
def extract_zip(params):
    """
    Estrae un file ZIP in una directory.
    params: {'zip_path': ..., 'extract_to': ...}
    """
    import zipfile
    zip_path = params.get('zip_path')
    extract_to = params.get('extract_to')
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        return {'result': 'ok'}
    except Exception as e:
        return {'error': str(e)}
def perform_file_action(params):
    """
    Esegue azioni su file: read, write, list.
    params: {'op': 'read'|'write'|'list', ...}
    """
    import os
    op = params.get('op')
    path = params.get('path')
    if op == 'read' and path:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return {'content': f.read()}
        except Exception as e:
            return {'error': str(e)}
    elif op == 'write' and path:
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(params.get('content', ''))
            return {'result': 'ok'}
        except Exception as e:
            return {'error': str(e)}
    elif op == 'list' and path:
        try:
            return {'files': os.listdir(path)}
        except Exception as e:
            return {'error': str(e)}
    elif op == 'copy':
        src = params.get('src')
        dst = params.get('dst')
        try:
            import shutil
            shutil.copy(src, dst)
            return {'result': 'ok'}
        except Exception as e:
            return {'error': str(e)}
    elif op == 'delete' and path:
        try:
            os.remove(path)
            return {'result': 'ok'}
        except Exception as e:
            return {'error': str(e)}
    elif op == 'rename':
        src = params.get('src')
        dst = params.get('dst')
        try:
            os.rename(src, dst)
            return {'result': 'ok'}
        except Exception as e:
            return {'error': str(e)}
    elif op == 'mkdir' and path:
        try:
            os.makedirs(path, exist_ok=True)
            return {'result': 'ok'}
        except Exception as e:
            return {'error': str(e)}
    return {'error': 'Operazione non valida'}
"""
Advanced File utilities for SuperAgent
Supports: reading, writing, appending, JSON, CSV, binary files, file operations
"""
from pathlib import Path
from typing import Optional, Union, List, Dict, Any
import json
import csv
import shutil
import os
import mimetypes
from datetime import datetime


class FileManager:
    """Advanced file management tool."""
    
    def __init__(self):
        self.encoding = 'utf-8'
    
    def read_file(self, path: str, encoding: str = None) -> Union[str, bytes, dict]:
        """
        Read file content. Auto-detects JSON files.
        
        Args:
            path: File path
            encoding: Text encoding (default: utf-8, None for binary)
            
        Returns:
            File content as string, bytes, or dict (for JSON)
        """
        try:
            p = Path(path)
            if not p.exists():
                return {"error": f"File non trovato: {path}"}
            
            # Check if JSON
            if p.suffix.lower() == '.json':
                with open(p, 'r', encoding=encoding or self.encoding) as f:
                    return json.load(f)
            
            # Binary mode
            if encoding is None:
                return p.read_bytes()
            
            # Text mode
            return p.read_text(encoding=encoding or self.encoding)
            
        except Exception as e:
            return {"error": f"Errore lettura file: {str(e)}"}
    
    def write_file(self, path: str, content: Union[str, bytes, dict, list], 
                   encoding: str = None, mode: str = 'w') -> dict:
        """
        Write content to file. Auto-handles JSON, CSV, text, binary.
        
        Args:
            path: File path
            content: Content to write
            encoding: Text encoding (default: utf-8, None for binary)
            mode: Write mode ('w' = overwrite, 'a' = append)
            
        Returns:
            Dict with status, path, size
        """
        try:
            p = Path(path)
            p.parent.mkdir(parents=True, exist_ok=True)
            
            # JSON
            if isinstance(content, (dict, list)):
                with open(p, mode, encoding=encoding or self.encoding) as f:
                    json.dump(content, f, indent=2, ensure_ascii=False)
            
            # Binary
            elif isinstance(content, bytes):
                with open(p, mode + 'b') as f:
                    f.write(content)
            
            # Text
            else:
                p.write_text(str(content), encoding=encoding or self.encoding)
            
            return {
                "status": "success",
                "path": str(p),
                "size": p.stat().st_size,
                "mode": mode
            }
            
        except Exception as e:
            return {"error": f"Errore scrittura file: {str(e)}"}
    
    def append_file(self, path: str, content: str, newline: bool = True) -> dict:
        """
        Append content to file.
        
        Args:
            path: File path
            content: Content to append
            newline: Add newline before content
            
        Returns:
            Dict with status
        """
        try:
            p = Path(path)
            with open(p, 'a', encoding=self.encoding) as f:
                if newline and p.exists() and p.stat().st_size > 0:
                    f.write('\n')
                f.write(content)
            
            return {"status": "success", "path": str(p)}
        except Exception as e:
            return {"error": f"Errore append: {str(e)}"}
    
    def read_lines(self, path: str, start_line: int = 0, end_line: int = None) -> List[str]:
        """
        Read specific lines from file.
        
        Args:
            path: File path
            start_line: Start line (0-indexed)
            end_line: End line (exclusive, None = to end)
            
        Returns:
            List of lines
        """
        try:
            p = Path(path)
            with open(p, 'r', encoding=self.encoding) as f:
                lines = f.readlines()
                return lines[start_line:end_line]
        except Exception as e:
            return [f"Error: {str(e)}"]
    
    def write_lines(self, path: str, lines: List[str]) -> dict:
        """Write list of lines to file."""
        content = '\n'.join(lines)
        return self.write_file(path, content)
    
    def read_json(self, path: str) -> Union[dict, list]:
        """Read and parse JSON file."""
        try:
            with open(path, 'r', encoding=self.encoding) as f:
                return json.load(f)
        except Exception as e:
            return {"error": f"Errore JSON: {str(e)}"}
    
    def write_json(self, path: str, data: Union[dict, list], indent: int = 2) -> dict:
        """Write data to JSON file."""
        try:
            p = Path(path)
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, 'w', encoding=self.encoding) as f:
                json.dump(data, f, indent=indent, ensure_ascii=False)
            return {"status": "success", "path": str(p)}
        except Exception as e:
            return {"error": f"Errore scrittura JSON: {str(e)}"}
    
    def read_csv(self, path: str, delimiter: str = ',') -> List[Dict[str, Any]]:
        """Read CSV file as list of dicts."""
        try:
            with open(path, 'r', encoding=self.encoding) as f:
                reader = csv.DictReader(f, delimiter=delimiter)
                return list(reader)
        except Exception as e:
            return [{"error": str(e)}]
    
    def write_csv(self, path: str, data: List[Dict[str, Any]], 
                  fieldnames: List[str] = None) -> dict:
        """Write list of dicts to CSV file."""
        try:
            p = Path(path)
            p.parent.mkdir(parents=True, exist_ok=True)
            
            if not data:
                return {"error": "No data to write"}
            
            if fieldnames is None:
                fieldnames = list(data[0].keys())
            
            with open(p, 'w', encoding=self.encoding, newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            return {"status": "success", "path": str(p)}
        except Exception as e:
            return {"error": f"Errore CSV: {str(e)}"}
    
    def list_dir(self, path: str, pattern: str = "*", recursive: bool = False) -> List[Dict[str, Any]]:
        """
        List directory contents with details.
        
        Args:
            path: Directory path
            pattern: Glob pattern (e.g., "*.py", "*.txt")
            recursive: Search recursively
            
        Returns:
            List of dicts with file info
        """
        try:
            p = Path(path)
            if not p.exists():
                return [{"error": "Directory not found"}]
            
            if recursive:
                items = p.rglob(pattern)
            else:
                items = p.glob(pattern)
            
            result = []
            for item in items:
                stat = item.stat()
                result.append({
                    "name": item.name,
                    "path": str(item),
                    "type": "dir" if item.is_dir() else "file",
                    "size": stat.st_size if item.is_file() else 0,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "extension": item.suffix
                })
            
            return result
        except Exception as e:
            return [{"error": str(e)}]
    
    def file_exists(self, path: str) -> bool:
        """Check if file exists."""
        return Path(path).exists()
    
    def file_info(self, path: str) -> Dict[str, Any]:
        """Get detailed file information."""
        try:
            p = Path(path)
            if not p.exists():
                return {"error": "File not found"}
            
            stat = p.stat()
            return {
                "path": str(p),
                "name": p.name,
                "extension": p.suffix,
                "size": stat.st_size,
                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "is_file": p.is_file(),
                "is_dir": p.is_dir(),
                "mime_type": mimetypes.guess_type(str(p))[0]
            }
        except Exception as e:
            return {"error": str(e)}
    
    def copy_file(self, src: str, dst: str) -> dict:
        """Copy file from src to dst."""
        try:
            Path(dst).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            return {"status": "success", "src": src, "dst": dst}
        except Exception as e:
            return {"error": f"Errore copia: {str(e)}"}
    
    def move_file(self, src: str, dst: str) -> dict:
        """Move/rename file."""
        try:
            Path(dst).parent.mkdir(parents=True, exist_ok=True)
            shutil.move(src, dst)
            return {"status": "success", "src": src, "dst": dst}
        except Exception as e:
            return {"error": f"Errore spostamento: {str(e)}"}
    
    def delete_file(self, path: str) -> dict:
        """Delete file or empty directory."""
        try:
            p = Path(path)
            if p.is_file():
                p.unlink()
            elif p.is_dir():
                p.rmdir()  # Only removes empty dirs
            else:
                return {"error": "Path not found"}
            
            return {"status": "success", "path": str(p)}
        except Exception as e:
            return {"error": f"Errore eliminazione: {str(e)}"}
    
    def create_directory(self, path: str) -> dict:
        """Create directory (and parents if needed)."""
        try:
            p = Path(path)
            p.mkdir(parents=True, exist_ok=True)
            return {"status": "success", "path": str(p)}
        except Exception as e:
            return {"error": str(e)}
    
    def search_files(self, directory: str, pattern: str, content_search: str = None) -> List[str]:
        """
        Search for files by name pattern and optionally content.
        
        Args:
            directory: Search directory
            pattern: Filename pattern (e.g., "*.py")
            content_search: Optional text to search in files
            
        Returns:
            List of matching file paths
        """
        try:
            p = Path(directory)
            matches = []
            
            for file in p.rglob(pattern):
                if file.is_file():
                    if content_search:
                        try:
                            content = file.read_text(encoding=self.encoding)
                            if content_search in content:
                                matches.append(str(file))
                        except:
                            continue
                    else:
                        matches.append(str(file))
            
            return matches
        except Exception as e:
            return [f"Error: {str(e)}"]
    
    def get_file_size(self, path: str, unit: str = 'bytes') -> Union[int, float]:
        """
        Get file size in specified unit.
        
        Args:
            path: File path
            unit: 'bytes', 'kb', 'mb', 'gb'
        """
        try:
            size = Path(path).stat().st_size
            
            if unit.lower() == 'kb':
                return round(size / 1024, 2)
            elif unit.lower() == 'mb':
                return round(size / (1024 * 1024), 2)
            elif unit.lower() == 'gb':
                return round(size / (1024 * 1024 * 1024), 2)
            
            return size
        except Exception as e:
            return -1


# Global instance and convenience functions
_file_manager = FileManager()

def read_file(path: str, encoding: str = 'utf-8') -> str:
    """Quick file read."""
    result = _file_manager.read_file(path, encoding)
    if isinstance(result, dict) and 'error' in result:
        return result['error']
    return result

def write_file(path: str, content: str, encoding: str = 'utf-8') -> Union[dict, str]:
    """Quick file write."""
    return _file_manager.write_file(path, content, encoding)

def append_file(path: str, content: str) -> dict:
    """Quick append."""
    return _file_manager.append_file(path, content)

def read_json(path: str) -> dict:
    """Quick JSON read."""
    return _file_manager.read_json(path)

def write_json(path: str, data: dict) -> dict:
    """Quick JSON write."""
    return _file_manager.write_json(path, data)

def list_dir(path: str, pattern: str = "*") -> list:
    """Quick directory listing."""
    return _file_manager.list_dir(path, pattern)

def file_exists(path: str) -> bool:
    """Quick existence check."""
    return _file_manager.file_exists(path)

def file_info(path: str) -> dict:
    """Quick file info."""
    return _file_manager.file_info(path)