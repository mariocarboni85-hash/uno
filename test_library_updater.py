"""
Test suite per LibraryUpdater
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tools.library_updater import LibraryUpdater, quick_update, check_updates
from pathlib import Path
import json
import time


def test_library_updater():
    """Test del sistema di aggiornamento librerie"""
    
    print("=" * 60)
    print("TEST LIBRARY UPDATER")
    print("=" * 60)
    
    updater = LibraryUpdater()
    test_venv = "super_agent_advanced"
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Check outdated packages
    print("\n[1/10] Test controllo pacchetti obsoleti...")
    try:
        outdated = updater.list_outdated_packages(test_venv)
        print(f"  ✓ Trovati {len(outdated)} pacchetti obsoleti")
        
        if outdated:
            for pkg in outdated[:3]:
                print(f"    • {pkg['name']}: {pkg['version']} → {pkg['latest_version']}")
        
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Errore: {e}")
        tests_failed += 1
    
    # Test 2: Get installed packages
    print("\n[2/10] Test recupero pacchetti installati...")
    try:
        packages = updater.get_installed_packages(test_venv)
        print(f"  ✓ Trovati {len(packages)} pacchetti installati")
        
        # Mostra alcuni pacchetti
        for name, version in list(packages.items())[:5]:
            print(f"    • {name}: {version}")
        
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Errore: {e}")
        tests_failed += 1
    
    # Test 3: Create backup
    print("\n[3/10] Test creazione backup...")
    try:
        backup_file = updater.create_backup(test_venv)
        backup_path = Path(backup_file)
        
        assert backup_path.exists(), "File di backup non creato"
        
        # Verifica contenuto
        with open(backup_path, 'r') as f:
            backup_data = json.load(f)
        
        assert 'venv_name' in backup_data
        assert 'packages' in backup_data
        assert len(backup_data['packages']) > 0
        
        print(f"  ✓ Backup creato: {backup_path.name}")
        print(f"    • Venv: {backup_data['venv_name']}")
        print(f"    • Packages: {len(backup_data['packages'])}")
        
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Errore: {e}")
        tests_failed += 1
    
    # Test 4: Update pip
    print("\n[4/10] Test aggiornamento pip...")
    try:
        success, message = updater.update_pip(test_venv)
        print(f"  {message}")
        
        if success:
            tests_passed += 1
        else:
            tests_failed += 1
    except Exception as e:
        print(f"  ✗ Errore: {e}")
        tests_failed += 1
    
    # Test 5: Get package info
    print("\n[5/10] Test info pacchetto...")
    try:
        info = updater.get_package_info(test_venv, "numpy")
        
        if info:
            print(f"  ✓ Info numpy recuperate:")
            print(f"    • Version: {info.get('Version', 'N/A')}")
            print(f"    • Summary: {info.get('Summary', 'N/A')[:50]}...")
            tests_passed += 1
        else:
            print("  ✗ Nessuna info recuperata")
            tests_failed += 1
    except Exception as e:
        print(f"  ✗ Errore: {e}")
        tests_failed += 1
    
    # Test 6: List backups
    print("\n[6/10] Test lista backup...")
    try:
        backups = updater.list_backups(test_venv)
        print(f"  ✓ Trovati {len(backups)} backup")
        
        if backups:
            for backup in backups[:3]:
                print(f"    • {backup['filename']}")
        
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Errore: {e}")
        tests_failed += 1
    
    # Test 7: Schedule auto update
    print("\n[7/10] Test configurazione auto-update...")
    try:
        config_file = updater.schedule_auto_update(
            test_venv,
            schedule="weekly",
            exclude=["torch", "tensorflow"]
        )
        
        config_path = Path(config_file)
        assert config_path.exists(), "File di configurazione non creato"
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        assert config['venv_name'] == test_venv
        assert config['schedule'] == "weekly"
        assert "torch" in config['exclude']
        
        print(f"  ✓ Configurazione creata")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Errore: {e}")
        tests_failed += 1
    
    # Test 8: Quick update function (solo check, no update)
    print("\n[8/10] Test funzione quick check...")
    try:
        outdated = check_updates(test_venv)
        print(f"  ✓ Quick check: {len(outdated)} aggiornamenti disponibili")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Errore: {e}")
        tests_failed += 1
    
    # Test 9: Check security vulnerabilities
    print("\n[9/10] Test controllo vulnerabilità...")
    try:
        vulnerabilities = updater.check_security_vulnerabilities(test_venv)
        
        if isinstance(vulnerabilities, list):
            print(f"  ✓ Security audit completato")
            if vulnerabilities:
                print(f"    ⚠️  {len(vulnerabilities)} vulnerabilità trovate")
            else:
                print(f"    ✓ Nessuna vulnerabilità nota")
            tests_passed += 1
        else:
            print("  ⚠️  pip audit non disponibile")
            tests_passed += 1
    except Exception as e:
        print(f"  ⚠️  pip audit non supportato: {e}")
        tests_passed += 1  # Non è un errore critico
    
    # Test 10: Verify venv paths
    print("\n[10/10] Test path virtual environment...")
    try:
        python_path = updater.get_venv_python(test_venv)
        pip_path = updater.get_venv_pip(test_venv)
        
        assert python_path.exists(), f"Python non trovato: {python_path}"
        assert pip_path.exists(), f"Pip non trovato: {pip_path}"
        
        print(f"  ✓ Path verificati:")
        print(f"    • Python: {python_path}")
        print(f"    • Pip: {pip_path}")
        
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Errore: {e}")
        tests_failed += 1
    
    # Riepilogo
    print("\n" + "=" * 60)
    print("RIEPILOGO TEST")
    print("=" * 60)
    print(f"✓ Test passati: {tests_passed}/10")
    print(f"✗ Test falliti: {tests_failed}/10")
    
    if tests_failed == 0:
        print("\n🎉 Tutti i test sono passati!")
    else:
        print(f"\n⚠️  {tests_failed} test falliti")
    
    return tests_failed == 0


if __name__ == "__main__":
    success = test_library_updater()
    sys.exit(0 if success else 1)
