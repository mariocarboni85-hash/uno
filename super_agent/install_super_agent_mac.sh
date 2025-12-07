#!/usr/bin/env bash
# Installer Super Agent per macOS

echo "Installazione Super Agent su macOS..."
# Verifica Python
if ! command -v python3 &> /dev/null; then
  echo "Python3 non trovato. Installalo da https://www.python.org/downloads/mac-osx/"
  exit 1
fi
# Installa Homebrew se mancante
if ! command -v brew &> /dev/null; then
  echo "Homebrew non trovato. Installazione..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi
# Installa dipendenze
brew install python3
pip3 install --upgrade pip
pip3 install flask requests psutil pyjwt
# Copia file
mkdir -p /usr/local/superagent
cp -R super_agent/* /usr/local/superagent/
# Avvio servizi (esempio con launchctl)
for s in auth_service executor trainer evaluator deployer env_builder dashboard; do
  launchctl load /usr/local/superagent/services/$s/$s.plist
  launchctl start $s
  done
echo "Installazione completata. Avvia Super Agent con launchctl o dal terminale."
