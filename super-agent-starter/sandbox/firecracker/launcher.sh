#!/usr/bin/env bash
set -e
# Avvia una VM Firecracker con la configurazione locale
firecracker --config-file sandbox/firecracker/fc_config.json
