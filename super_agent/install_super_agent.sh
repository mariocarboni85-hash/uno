#!/usr/bin/env bash
echo "Installazione Super Agent..."
sudo apt update
sudo apt install -y python3 python3-pip
pip3 install --upgrade pip
pip3 install flask requests psutil pyjwt
sudo cp -r super_agent /opt/superagent
SERVICES=("auth_service" "executor" "trainer" "evaluator" "deployer" "env_builder" "dashboard")
for s in "${SERVICES[@]}"; do
  sudo cp ./services/$s/$s.service /etc/systemd/system/
  sudo systemctl enable $s
  sudo systemctl start $s
done
echo "Installazione completata. Avvia Super Agent con: sudo systemctl start dashboard"
