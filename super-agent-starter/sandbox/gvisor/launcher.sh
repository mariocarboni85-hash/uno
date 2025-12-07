#!/usr/bin/env bash
set -e
# Avvia un container gVisor con la configurazione locale
runsc --root=sandbox/gvisor run --config sandbox/gvisor/gvisor_config.json my_sandboxed_app
