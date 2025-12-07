"""
Library Updater - Sistema di Aggiornamento Automatico Librerie
Gestisce aggiornamenti automatici, controllo versioni, e rollback
"""

import subprocess
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import venv
import sys


class LibraryUpdater:
    """Gestisce aggiornamenti automatici delle librerie Python"""
    
    def __init__(self, venvs_dir: str = "venvs"):
        """
        Inizializza il Library Updater
        
        Args:
            venvs_dir: Directory contenente i virtual environments
        """
        self.base_dir = Path.cwd()
        self.venvs_dir = self.base_dir / venvs_dir
        self.updates_log_dir = self.base_dir / "updates_logs"
        self.updates_log_dir.mkdir(exist_ok=True)
        self.backup_dir = self.updates_log_dir  # Alias per compatibilità
        
    def get_venv_python(self, venv_name: str) -> Path:
        """Ottiene il path dell'eseguibile Python in un venv"""
        venv_path = self.venvs_dir / venv_name
        if os.name == 'nt':
            return venv_path / "Scripts" / "python.exe"
        return venv_path / "bin" / "python"
    
    def get_venv_pip(self, venv_name: str) -> Path:
        """Ottiene il path dell'eseguibile pip in un venv"""
        venv_path = self.venvs_dir / venv_name
        if os.name == 'nt':
            return venv_path / "Scripts" / "pip.exe"
        return venv_path / "bin" / "pip"
    
    def list_outdated_packages(self, venv_name: str) -> List[Dict[str, str]]:
        """
        Elenca i pacchetti con aggiornamenti disponibili
        
        Args:
            venv_name: Nome del virtual environment
            
        Returns:
            Lista di dizionari con info sui pacchetti obsoleti
        """
        pip_path = self.get_venv_pip(venv_name)
        
        if not pip_path.exists():
            raise ValueError(f"Virtual environment '{venv_name}' non trovato")
        
        try:
            # Usa pip list --outdated --format json
            result = subprocess.run(
                [str(pip_path), "list", "--outdated", "--format", "json"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                outdated = json.loads(result.stdout)
                return outdated
            else:
                print(f"Errore: {result.stderr}")
                return []
                
        except subprocess.TimeoutExpired:
            print("Timeout durante il controllo pacchetti obsoleti")
            return []
        except json.JSONDecodeError:
            print("Errore nel parsing dell'output pip")
            return []
        except Exception as e:
            print(f"Errore: {e}")
            return []
    
    def get_installed_packages(self, venv_name: str) -> Dict[str, str]:
        """
        Ottiene lista di tutti i pacchetti installati con versioni
        
        Args:
            venv_name: Nome del virtual environment
            
        Returns:
            Dict {package_name: version}
        """
        pip_path = self.get_venv_pip(venv_name)
        
        try:
            result = subprocess.run(
                [str(pip_path), "list", "--format", "json"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                packages = json.loads(result.stdout)
                return {pkg['name']: pkg['version'] for pkg in packages}
            return {}
            
        except Exception as e:
            print(f"Errore nel recupero pacchetti: {e}")
            return {}
    
    def create_backup(self, venv_name: str) -> str:
        """
        Crea un backup delle versioni correnti prima dell'aggiornamento
        
        Args:
            venv_name: Nome del virtual environment
            
        Returns:
            Path del file di backup
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.updates_log_dir / f"backup_{venv_name}_{timestamp}.json"
        
        packages = self.get_installed_packages(venv_name)
        
        backup_data = {
            "venv_name": venv_name,
            "timestamp": timestamp,
            "date": datetime.now().isoformat(),
            "packages": packages,
            "total_packages": len(packages)
        }
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Backup creato: {backup_file.name}")
        return str(backup_file)
    
    def update_package(
        self, 
        venv_name: str, 
        package_name: str,
        specific_version: Optional[str] = None,
        timeout: int = 300
    ) -> Tuple[bool, str]:
        """
        Aggiorna un singolo pacchetto
        
        Args:
            venv_name: Nome del virtual environment
            package_name: Nome del pacchetto da aggiornare
            specific_version: Versione specifica (None = ultima)
            timeout: Timeout in secondi
            
        Returns:
            (successo, messaggio)
        """
        pip_path = self.get_venv_pip(venv_name)
        
        if specific_version:
            install_spec = f"{package_name}=={specific_version}"
        else:
            install_spec = f"{package_name} --upgrade"
        
        try:
            result = subprocess.run(
                [str(pip_path), "install"] + install_spec.split(),
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.returncode == 0:
                return True, f"✓ {package_name} aggiornato con successo"
            else:
                return False, f"✗ Errore aggiornamento {package_name}: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            return False, f"✗ Timeout aggiornamento {package_name}"
        except Exception as e:
            return False, f"✗ Errore: {e}"
    
    def update_all_packages(
        self, 
        venv_name: str,
        exclude: Optional[List[str]] = None,
        create_backup: bool = True
    ) -> Dict[str, Any]:
        """
        Aggiorna tutti i pacchetti obsoleti
        
        Args:
            venv_name: Nome del virtual environment
            exclude: Lista di pacchetti da escludere
            create_backup: Se True, crea backup prima dell'aggiornamento
            
        Returns:
            Dizionario con risultati dell'aggiornamento
        """
        exclude = exclude or []
        
        print(f"\n🔍 Controllo aggiornamenti per '{venv_name}'...")
        
        # Backup
        backup_file = None
        if create_backup:
            backup_file = self.create_backup(venv_name)
        
        # Lista pacchetti obsoleti
        outdated = self.list_outdated_packages(venv_name)
        
        if not outdated:
            print("✓ Tutti i pacchetti sono aggiornati!")
            return {
                "status": "up_to_date",
                "backup_file": backup_file,
                "updated": [],
                "failed": [],
                "skipped": []
            }
        
        print(f"\n📦 Trovati {len(outdated)} pacchetti da aggiornare")
        
        # Filtra pacchetti esclusi
        to_update = [pkg for pkg in outdated if pkg['name'] not in exclude]
        skipped = [pkg for pkg in outdated if pkg['name'] in exclude]
        
        if skipped:
            print(f"⏭️  Saltati {len(skipped)} pacchetti: {', '.join(p['name'] for p in skipped)}")
        
        # Aggiorna
        updated = []
        failed = []
        
        for i, pkg in enumerate(to_update, 1):
            name = pkg['name']
            current = pkg['version']
            latest = pkg['latest_version']
            
            print(f"\n[{i}/{len(to_update)}] Aggiornamento {name}: {current} → {latest}")
            
            success, message = self.update_package(venv_name, name)
            print(f"  {message}")
            
            if success:
                updated.append({
                    "name": name,
                    "old_version": current,
                    "new_version": latest
                })
            else:
                failed.append({
                    "name": name,
                    "version": current,
                    "error": message
                })
        
        # Log risultati
        log_file = self._save_update_log(
            venv_name, updated, failed, skipped, backup_file
        )
        
        # Riepilogo
        print(f"\n{'='*60}")
        print("📊 RIEPILOGO AGGIORNAMENTO")
        print(f"{'='*60}")
        print(f"✓ Aggiornati: {len(updated)}")
        print(f"✗ Falliti: {len(failed)}")
        print(f"⏭️  Saltati: {len(skipped)}")
        print(f"📝 Log salvato: {log_file}")
        
        if updated:
            print(f"\n✓ Pacchetti aggiornati:")
            for pkg in updated:
                print(f"  • {pkg['name']}: {pkg['old_version']} → {pkg['new_version']}")
        
        if failed:
            print(f"\n✗ Aggiornamenti falliti:")
            for pkg in failed:
                print(f"  • {pkg['name']}: {pkg['error']}")
        
        return {
            "status": "completed",
            "backup_file": backup_file,
            "log_file": log_file,
            "updated": updated,
            "failed": failed,
            "skipped": skipped,
            "total_outdated": len(outdated)
        }
    
    def rollback_from_backup(self, backup_file: str) -> Dict[str, Any]:
        """
        Ripristina le versioni da un file di backup
        
        Args:
            backup_file: Path del file di backup
            
        Returns:
            Dizionario con risultati del rollback
        """
        backup_path = Path(backup_file)
        
        if not backup_path.exists():
            return {"status": "error", "message": "File di backup non trovato"}
        
        try:
            with open(backup_path, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            venv_name = backup_data['venv_name']
            packages = backup_data['packages']
            
            print(f"\n🔄 Rollback per '{venv_name}' dal backup {backup_data['date']}")
            print(f"📦 {len(packages)} pacchetti da ripristinare")
            
            restored = []
            failed = []
            
            for i, (name, version) in enumerate(packages.items(), 1):
                print(f"[{i}/{len(packages)}] Ripristino {name}=={version}")
                
                success, message = self.update_package(
                    venv_name, name, specific_version=version
                )
                
                if success:
                    restored.append({"name": name, "version": version})
                else:
                    failed.append({"name": name, "version": version, "error": message})
            
            print(f"\n✓ Ripristinati: {len(restored)}")
            print(f"✗ Falliti: {len(failed)}")
            
            return {
                "status": "completed",
                "restored": restored,
                "failed": failed,
                "backup_file": str(backup_path)
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def update_pip(self, venv_name: str) -> Tuple[bool, str]:
        """
        Aggiorna pip all'ultima versione
        
        Args:
            venv_name: Nome del virtual environment
            
        Returns:
            (successo, messaggio)
        """
        python_path = self.get_venv_python(venv_name)
        
        try:
            result = subprocess.run(
                [str(python_path), "-m", "pip", "install", "--upgrade", "pip"],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                return True, "✓ pip aggiornato con successo"
            else:
                return False, f"✗ Errore aggiornamento pip: {result.stderr}"
                
        except Exception as e:
            return False, f"✗ Errore: {e}"
    
    def check_security_vulnerabilities(self, venv_name: str) -> List[Dict[str, Any]]:
        """
        Controlla vulnerabilità di sicurezza usando pip audit
        
        Args:
            venv_name: Nome del virtual environment
            
        Returns:
            Lista di vulnerabilità trovate
        """
        pip_path = self.get_venv_pip(venv_name)
        
        try:
            # Prova pip audit (disponibile da pip 23.3+)
            result = subprocess.run(
                [str(pip_path), "audit", "--format", "json"],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                audit_data = json.loads(result.stdout)
                return audit_data.get('vulnerabilities', [])
            else:
                print("pip audit non disponibile o nessuna vulnerabilità trovata")
                return []
                
        except subprocess.TimeoutExpired:
            print("Timeout durante audit di sicurezza")
            return []
        except json.JSONDecodeError:
            # pip audit potrebbe non essere disponibile
            return []
        except Exception as e:
            print(f"Errore durante audit: {e}")
            return []
    
    def get_package_info(self, venv_name: str, package_name: str) -> Dict[str, Any]:
        """
        Ottiene informazioni dettagliate su un pacchetto
        
        Args:
            venv_name: Nome del virtual environment
            package_name: Nome del pacchetto
            
        Returns:
            Dizionario con info del pacchetto
        """
        pip_path = self.get_venv_pip(venv_name)
        
        try:
            result = subprocess.run(
                [str(pip_path), "show", package_name],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                info = {}
                for line in result.stdout.strip().split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        info[key.strip()] = value.strip()
                return info
            return {}
            
        except Exception as e:
            print(f"Errore nel recupero info pacchetto: {e}")
            return {}
    
    def list_backups(self, venv_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Elenca i backup disponibili
        
        Args:
            venv_name: Filtra per venv specifico (None = tutti)
            
        Returns:
            Lista di backup disponibili
        """
        backups = []
        
        for backup_file in self.updates_log_dir.glob("backup_*.json"):
            try:
                with open(backup_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if venv_name is None or data['venv_name'] == venv_name:
                    backups.append({
                        "file": str(backup_file),
                        "filename": backup_file.name,
                        "venv_name": data['venv_name'],
                        "date": data['date'],
                        "total_packages": data['total_packages']
                    })
            except Exception:
                continue
        
        # Ordina per data (più recenti prima)
        backups.sort(key=lambda x: x['date'], reverse=True)
        return backups
    
    def schedule_auto_update(
        self, 
        venv_name: str,
        schedule: str = "weekly",
        exclude: Optional[List[str]] = None
    ) -> str:
        """
        Prepara configurazione per aggiornamenti automatici schedulati
        
        Args:
            venv_name: Nome del virtual environment
            schedule: Frequenza (daily, weekly, monthly)
            exclude: Pacchetti da escludere
            
        Returns:
            Path del file di configurazione
        """
        config = {
            "venv_name": venv_name,
            "schedule": schedule,
            "exclude": exclude or [],
            "enabled": True,
            "create_backup": True,
            "last_update": None,
            "created_at": datetime.now().isoformat()
        }
        
        config_file = self.updates_log_dir / f"auto_update_{venv_name}.json"
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Configurazione auto-update salvata: {config_file.name}")
        print(f"  • Venv: {venv_name}")
        print(f"  • Schedule: {schedule}")
        print(f"  • Exclude: {len(exclude or [])}")
        
        return str(config_file)
    
    def _save_update_log(
        self,
        venv_name: str,
        updated: List[Dict],
        failed: List[Dict],
        skipped: List[Dict],
        backup_file: Optional[str]
    ) -> str:
        """Salva log dell'aggiornamento"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.updates_log_dir / f"update_log_{venv_name}_{timestamp}.json"
        
        log_data = {
            "venv_name": venv_name,
            "timestamp": timestamp,
            "date": datetime.now().isoformat(),
            "backup_file": backup_file,
            "summary": {
                "updated": len(updated),
                "failed": len(failed),
                "skipped": len(skipped),
                "total": len(updated) + len(failed) + len(skipped)
            },
            "updated_packages": updated,
            "failed_packages": failed,
            "skipped_packages": skipped
        }
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)
        
        return str(log_file)


# Funzioni di utilità rapide

def quick_update(venv_name: str = "super_agent_advanced", exclude: Optional[List[str]] = None) -> Dict:
    """Aggiornamento rapido di un ambiente"""
    updater = LibraryUpdater()
    return updater.update_all_packages(venv_name, exclude=exclude)


def check_updates(venv_name: str = "super_agent_advanced") -> List[Dict]:
    """Controlla solo quali aggiornamenti sono disponibili"""
    updater = LibraryUpdater()
    return updater.list_outdated_packages(venv_name)


def rollback(backup_file: str) -> Dict:
    """Rollback rapido da backup"""
    updater = LibraryUpdater()
    return updater.rollback_from_backup(backup_file)


if __name__ == "__main__":
    # Esempio: aggiornamento automatico
    updater = LibraryUpdater()
    
    venv_name = "super_agent_advanced"
    
    print("=" * 60)
    print("LIBRARY UPDATER - Sistema Aggiornamento Automatico")
    print("=" * 60)
    
    # Aggiorna pip prima
    print("\n1️⃣  Aggiornamento pip...")
    success, msg = updater.update_pip(venv_name)
    print(msg)
    
    # Controlla pacchetti obsoleti
    print("\n2️⃣  Controllo pacchetti obsoleti...")
    outdated = updater.list_outdated_packages(venv_name)
    
    if outdated:
        print(f"\n📦 {len(outdated)} pacchetti con aggiornamenti disponibili:")
        for pkg in outdated[:10]:  # Mostra primi 10
            print(f"  • {pkg['name']}: {pkg['version']} → {pkg['latest_version']}")
        
        if len(outdated) > 10:
            print(f"  ... e altri {len(outdated) - 10} pacchetti")
        
        # Chiedi conferma
        print(f"\n3️⃣  Vuoi aggiornare tutti i {len(outdated)} pacchetti? (y/n)")
        response = input(">>> ").strip().lower()
        
        if response == 'y':
            # Pacchetti da escludere (opzionale)
            exclude = []  # es: ['torch', 'tensorflow']
            
            # Esegui aggiornamento
            result = updater.update_all_packages(
                venv_name, 
                exclude=exclude,
                create_backup=True
            )
            
            print(f"\n✅ Aggiornamento completato!")
            print(f"   Backup: {result['backup_file']}")
            print(f"   Log: {result['log_file']}")
        else:
            print("Aggiornamento annullato.")
    else:
        print("✓ Tutti i pacchetti sono già aggiornati!")
    
    # Mostra backup disponibili
    print(f"\n4️⃣  Backup disponibili:")
    backups = updater.list_backups(venv_name)
    if backups:
        for backup in backups[:5]:
            print(f"  • {backup['filename']}")
            print(f"    Data: {backup['date']}")
            print(f"    Packages: {backup['total_packages']}")
    else:
        print("  Nessun backup trovato")
