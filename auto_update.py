"""
Auto Update Script - Aggiorna automaticamente tutte le librerie
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from tools.library_updater import LibraryUpdater


def main():
    """Aggiorna automaticamente tutte le librerie"""
    
    print("=" * 70)
    print("AUTO UPDATE - Aggiornamento Automatico Librerie Super Agent")
    print("=" * 70)
    
    updater = LibraryUpdater()
    venv_name = "super_agent_advanced"
    
    # Pacchetti da escludere (opzionale - rimuovi commento se necessario)
    exclude = [
        # "torch",          # PyTorch - aggiornamenti molto grandi
        # "tensorflow",     # TensorFlow - aggiornamenti molto grandi
        # "transformers",   # HuggingFace - aggiornamenti frequenti
    ]
    
    try:
        # Step 1: Aggiorna pip
        print("\n📦 Step 1/3: Aggiornamento pip...")
        success, message = updater.update_pip(venv_name)
        print(f"  {message}")
        
        # Step 2: Controlla aggiornamenti disponibili
        print("\n🔍 Step 2/3: Controllo aggiornamenti disponibili...")
        outdated = updater.list_outdated_packages(venv_name)
        
        if not outdated:
            print("  ✓ Tutte le librerie sono già aggiornate!")
            print("\n✅ Nessun aggiornamento necessario.")
            return 0
        
        print(f"  📊 Trovati {len(outdated)} pacchetti da aggiornare:")
        print()
        
        # Mostra lista completa
        for i, pkg in enumerate(outdated, 1):
            print(f"    {i:2d}. {pkg['name']:25s} {pkg['version']:15s} → {pkg['latest_version']}")
        
        # Step 3: Esegui aggiornamento
        print(f"\n⚡ Step 3/3: Aggiornamento in corso...")
        print(f"  • Backup: Sì")
        print(f"  • Pacchetti esclusi: {len(exclude)}")
        print()
        
        result = updater.update_all_packages(
            venv_name,
            exclude=exclude,
            create_backup=True
        )
        
        # Riepilogo finale
        print("\n" + "=" * 70)
        print("✅ AGGIORNAMENTO COMPLETATO")
        print("=" * 70)
        
        print(f"\n📊 Statistiche:")
        print(f"  • Pacchetti aggiornati: {len(result['updated'])}")
        print(f"  • Aggiornamenti falliti: {len(result['failed'])}")
        print(f"  • Pacchetti saltati: {len(result['skipped'])}")
        print(f"  • Totale pacchetti obsoleti: {result['total_outdated']}")
        
        print(f"\n📁 File generati:")
        print(f"  • Backup: {result['backup_file']}")
        print(f"  • Log: {result['log_file']}")
        
        if result['updated']:
            print(f"\n✓ Librerie aggiornate con successo:")
            for pkg in result['updated']:
                print(f"  • {pkg['name']:25s} {pkg['old_version']:15s} → {pkg['new_version']}")
        
        if result['failed']:
            print(f"\n⚠️  Aggiornamenti falliti:")
            for pkg in result['failed']:
                print(f"  • {pkg['name']}: {pkg['error']}")
        
        print(f"\n💡 Suggerimenti:")
        print(f"  • Per rollback: python -c \"from tools.library_updater import rollback; rollback('{result['backup_file']}')\"")
        print(f"  • Per vedere log: type {result['log_file']}")
        
        print("\n🎉 Super Agent è ora aggiornato con le ultime librerie!")
        
        return 0 if len(result['failed']) == 0 else 1
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Aggiornamento interrotto dall'utente")
        return 1
    except Exception as e:
        print(f"\n❌ Errore durante aggiornamento: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
