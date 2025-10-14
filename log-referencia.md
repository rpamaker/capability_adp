# To Deploy the app for the first time:

az login

[2] *  Microsoft Azure Sponsorship  5f11f4d0-5a98-4781-b993-3325488ef8e0  rpamaker.com

<!-- ## Create the Group -->
<!-- az group create --name AzureFunctionsQuickstart-rg --location eastus -->

## Create storage
az storage account create --name capabilitycliente --location eastus --resource-group AzureFunctionsQuickstart-rg --sku Standard_LRS

az functionapp create --resource-group AzureFunctionsQuickstart-rg --consumption-plan-location westeurope --runtime python --runtime-version 3.11 --functions-version 4 --name capability-cliente --os-type linux --storage-account capabilitycliente

## Correr local
func start

# Para hacer deploy
func azure functionapp publish capability-cliente

## Result:
Invoke url: https://capability-cliente.azurewebsites.net/api/http_trigger

