# Deploy Super Agent su Azure VM + Blob Storage
# Prerequisiti: Azure CLI configurato

$resourceGroup = "superAgentRG"
$location = "westeurope"
$vmName = "superAgentVM"
$storageAccount = "superagentstorage"

# Crea resource group
az group create --name $resourceGroup --location $location

# Crea VM
az vm create --resource-group $resourceGroup --name $vmName --image UbuntuLTS --size Standard_B2s --admin-username azureuser --generate-ssh-keys

# Crea storage account
az storage account create --name $storageAccount --resource-group $resourceGroup --location $location --sku Standard_LRS

# Crea container blob
az storage container create --account-name $storageAccount --name backend
az storage container create --account-name $storageAccount --name frontend

Write-Host "Deploy completato su Azure VM + Blob Storage"