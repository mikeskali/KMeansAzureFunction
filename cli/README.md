# KMeans Azure Function CLI client

## Prepare
* As a prerequisite, you should have Python 3.7 and up installed.
* run pip install -r requirements.txt

As an alternative(if you don't want to manage Python environments and dependencies installation), 
you can run the cli in a Docker. See Docker section. 

 ## Usage
 kmeans_cli.py SERVICE_URL DATA_PATH CLUSTERS <flags>
  optional flags:        --separator | --col_from | --col_to
 
 | Parameter | Description                                                | Sample Value | Default Value | Mandatory? |
|-----------|------------------------------------------------------------------------------------|------|------------|------------|
|SERVICE_URL|URL of the azure function                                                           |http://localhost:7071/api/KMeansHTTPTrigger|   | yes  | 
|DATA_PATH  |Data path of the input file                                                         |../SampleDataSets/iris.csv| |yes|
| clusters  | Number of clusters returned by the KMeans algorithm                                | 3    |            | Yes        |
| separator | Your input columns delimiter                                                       | \t   | ,          | No         |
| col_from  | If you don't want to use all the columns, set to first valid(numeric) column index | 0    | 0          | No         |
| col_to    | If you don't want to use all the columns, set to last valid(numeric) column index  | 5    | Last Column| No         |

 
 Example: `python kmeans_cli.py http://localhost:7071/api/KMeansHttpTrigger ../SampleDataSets/iris.csv --clusters 3 --col_from 0 --col_to 3`
 
 ### More on usage
 This CLI is using [python-fire](https://github.com/google/python-fire/blob/master/docs/using-cli.md#interactive-flag), see the link for additional usage patterns.
 
 ## Run in Docker
 * build the container: `docker build -t kmeans-cli .`
 * Before running the docker container: 
   * Please note, you will need to make your input file accessible in the container (see the `-v` in the sample below)
   * in case your docker container needs to communicate with your local host, specify the address as `host.docker.internal`. 
   Not needed if you are accessing the function running on Azure. This method was tested on MAC and should work for Windows as well.
   If it doesnt work on Linux, you may need to pass the `--network="host"` argument to the docker run command and specify 127.0.0.1 for localhost. 
 * Sample run with docker:  
   `docker run -v $(shell pwd)/../SampleDataSets/iris.csv:/app/input/input.csv kmeans-cli python kmeans_cli.py http://host.docker.internal:7071/api/KMeansHttpTrigger /app/input/input.csv --clusters 3 --col_from 0 --col_to 4`