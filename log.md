# To Deploy the app for the first time:

az login

[2] *  Microsoft Azure Sponsorship  5f11f4d0-5a98-4781-b993-3325488ef8e0  rpamaker.com

<!-- ## Create the Group -->
<!-- az group create --name AzureFunctionsQuickstart-rg --location eastus -->

## Create storage
az storage account create --name capabilityadp --location eastus --resource-group AzureFunctionsQuickstart-rg --sku Standard_LRS

az functionapp create --resource-group AzureFunctionsQuickstart-rg --consumption-plan-location westeurope --runtime python --runtime-version 3.11 --functions-version 4 --name capability-adp --os-type linux --storage-account capabilityadp

## Correr local
func start

## Para hacer deploy
func azure functionapp publish capability-adp

## Result:
Invoke url: https://capability-adp.azurewebsites.net/api/http_trigger_echo

# Para subir un update
func azure functionapp publish capability-adp

# Configuracion del capabilty en backend
## Creo el capability en backend
https://backend.pometrix.com/admin/document/capability/
https://backend.pometrix.com/admin/document/capability/15/change/

## Seteo el capability en el document-type
https://backend.pometrix.com/admin/document/documenttype/
https://backend.pometrix.com/admin/document/documenttype/57/change/

# Pruebas
Hago una prueba y copio el capability excecution para poder iterar local
https://backend.pometrix.com/admin/document/capabilityexecution/


# Agrego logica

## Prompt
Add a new endpoing similar as http_trigger_echo that respond with the request but with some changes:

if "proveedor_nombre" = "OSE" then
    If "domicilio" is similar as "DOLORES, SORIANO" then remove all lines and add 2 lines
            {
                "monto": [subtotal_gravado_22],
                "cantidad": 1,
                "p_unitario": [subtotal_gravado_22],
                "descripcion": "Otros gastos de estructura (AD)",
                "articulo":13360
            },
            {
                "monto": [no_facturable],
                "cantidad": -1,
                "p_unitario": [no_facturable],
                "descripcion": "Gastos no deducibles (AD)",
                "articulo":13371
            },
else if "domicilio" is similar as "YOUNG, RIO NEGRO" then remove all lines and add 3 lines
            {
                "monto": [subtotal_gravado_22 * 0.8],
                "cantidad": 0.8,
                "p_unitario": [subtotal_gravado_22  * 0.8],
                "descripcion": "Otros gastos de estructura (IN)",
                "articulo":12228
            },
            {
                "monto": [subtotal_gravado_22 * 0.1],
                "cantidad": 0.1,
                "p_unitario": [subtotal_gravado_22  * 0.1],
                "descripcion": "Otros gastos de estructura (SE)",
                "articulo":12891
            },
            {
                "monto": [subtotal_gravado_22 * 0.1],
                "cantidad": 0.1,
                "p_unitario": [subtotal_gravado_22  * 0.1],
                "descripcion": "Otros gastos de estructura (LO)",
                "articulo":12571
            },
            {
                "monto": [no_facturable],
                "cantidad": 1,
                "p_unitario": [no_facturable],
                "descripcion": "Gastos no deducibles (AD)",
                "articulo":13371
            },

Read the file test/payload_ose_t5.json to understand how the req_body strucutre is




Nota: agregar signo en cantidad de no_facturable