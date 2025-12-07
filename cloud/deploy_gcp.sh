#!/bin/bash
# Deploy Super Agent su Google Cloud VM + Storage
# Prerequisiti: gcloud CLI configurato

PROJECT_ID="super-agent-project"
ZONE="europe-west1-b"
VM_NAME="super-agent-vm"
BUCKET_NAME="super-agent-storage"

# Crea bucket
gsutil mb -l $ZONE gs://$BUCKET_NAME

# Avvia VM
gcloud compute instances create $VM_NAME --zone=$ZONE --machine-type=e2-medium --image-family=ubuntu-2004-lts --image-project=ubuntu-os-cloud

echo "VM avviata: $VM_NAME"

# Carica file su bucket
gsutil -m cp -r ../dashboard/backend gs://$BUCKET_NAME/backend/
gsutil -m cp -r ../dashboard/frontend gs://$BUCKET_NAME/frontend/

echo "Deploy completato su Google Cloud VM + Storage"