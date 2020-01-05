# KMeans Azure Function CLI client

## Prepare
* As a prerequisite, you should have Python 3.7 and up installed.
* run pip install -r requirements.txt

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