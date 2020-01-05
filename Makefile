#!/usr/bin/make -f
# ----------------------------------------------------------------------
#

run-locally:
	func host start

send-sample-request-jq:
	curl --data-binary "@SampleDataSets/iris.csv" 'http://localhost:7071/api/KMeansHttpTrigger?clusters=3&col_from=0&col_to=4&separator=,' | jq


run-cli-request:
	python cli/kmeans_cli.py http://localhost:7071/api/KMeansHttpTrigger SampleDataSets/iris.csv --clusters 3 --col_from 0 --col_to 4

create-azure-app:
	az group create --name KMeansAzureFunctionRG --location westeurope && \
	az storage account create --name msklyarkmeansfunctionstorage --location westeurope --resource-group KMeansAzureFunctionRG --sku Standard_LRS && \
	az functionapp create --resource-group KMeansAzureFunctionRG --os-type Linux --consumption-plan-location westeurope  --runtime python --runtime-version 3.7 --name KMeansAzureFunction --storage-account kmeansfunctionstorage

deploy-to-azure:
	func azure functionapp publish KMeansAzureFunction