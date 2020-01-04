# Azure Function KMeans

A simple Azure Python Function running a KMeans algorithm. 
The function is triggered by an HTTP request. 
HTTP request will include a features matrix and specify the number of clusters.   

## API
HTTP Request:
	post	/api/KMeansHttpTrigger

## Build and deploy
### Prerequisites
See [Azure Python Function quick start](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-python)
1. Make sure you have Python 3.7 installed
3. Install [Azure Functions Core tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local#v2)
4. Install [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
5. If you want to Deploy this function to Azure, you should have an active Azure subscription
6. Clone the repository
7. Activate Python 3.7 virtual environment

## Run and deploy
1. Run function locally: `func host start`
  
   You will get a localhost link (Something like `HttpTrigger: http://localhost:7071/api/HttpTrigger `).
   Now you can test the classification algorithm!
   
* Deploy function to Azure cloud: 

  * you should be logged in to Azure (if you are not, run `az login`)
  * Prepare for first deploy:  
  	You need to create resources, storage and Azure Function application. Note the `<>`, you need to replace with your values.  
  	
    * Create resource group (`az group create --name <SOME_RESOURCE_GROUP_NAME> --location westeurope`)
    * Create storage account (`az storage account create --name <somestoragename> --location westeurope --resource-group <SOME_RESOURCE_GROUP_NAME> --sku Standard_LRS`)
    * Create the function App. (`az functionapp create --resource-group <SOME_RESOURCE_GROUP_NAME> --os-type Linux \
--consumption-plan-location westeurope  --runtime python --runtime-version 3.7 \
--name <APP_NAME> --storage-account   <somestoragename> `)
  * Deploy to Azure: `func azure functionapp publish <APP_NAME>`

## API
The function expects a POST request with binary, utf8 data and a few parameters:
 
| Parameter | Description                                                | Sample Value | Default Value | Mandatory? |
|-----------|------------------------------------------------------------------------------------|------|------------|------------|
| clusters  | Number of clusters returned by the KMeans algorithm                                | 3    |            | Yes        |
| separator | Your input columns delimiter                                                       | \t   | ,          | No         |
| col_from  | If you don't want to use all the columns, set to first valid(numeric) column index | 0    | 0          | No         |
| col_to    | If you don't want to use all the columns, set to last valid(numeric) column index  | 5    | Last Column| No         |
 
### Sample Request (Linux / Mac)
`curl --data-binary "@SampleDataSets/iris.csv" 'http://localhost:7071/api/KMeansHttpTrigger?clusters=3&col_from=0&col_to=3&separator=,'`

You can download curl for windows as well ([Curl Windows Download](https://curl.haxx.se/windows/)) 


