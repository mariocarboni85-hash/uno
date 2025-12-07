# Gestione Ambienti SuperAgent

## Struttura
- `venv_nncf`: ambiente per moduli nncf, torch_pruning, torch
- `venv_scientific`: ambiente per tensorflow, scikit-image, opencv-python, numpy, scipy, networkx, pandas, matplotlib

## Setup rapido

### Ambiente nncf
1. Esegui `envs\setup_venv_nncf.ps1` da PowerShell
2. Attiva l’ambiente: `.\venv_nncf\Scripts\Activate.ps1`
3. Installa le dipendenze: `pip install -r envs\requirements_nncf.txt`

### Ambiente scientifico
1. Esegui `envs\setup_venv_scientific.ps1` da PowerShell
2. Attiva l’ambiente: `.\venv_scientific\Scripts\Activate.ps1`
3. Installa le dipendenze: `pip install -r envs\requirements_scientific.txt`

## Note
- Usa l’ambiente giusto per ogni script: moduli avanzati (pruning, compressione, automazione neurale) in `venv_nncf`, moduli scientifici e di analisi in `venv_scientific`.
- Consulta la documentazione dei singoli script per sapere quale ambiente usare.
