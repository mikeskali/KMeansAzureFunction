import logging
import json
from io import StringIO
import azure.functions as func
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # mandatory parameters
    try:
        file_sent = req.get_body()
        csv_data = file_sent.decode("utf-8")
    except Exception as e:
        logging.error("Failed parsing the body: %s", e)
        return create_error_response(400, "There was an error with data parsing: %s" % e)

    try:
        clusters = int(req.params.get('clusters'))
    except Exception as e:
        logging.error("Failed retrieving <clusters> parameter: %s" % e)
        return create_error_response(400, "Failed retrieving <clusters> parameter: %s" % e)

    # optional parameters
    col_from = req.params.get('col_from')
    col_to = req.params.get('col_to')
    separator = req.params.get('separator', ",")

    logging.info("Request data: data_size=%s, #of clusters=%s, col_from=%s, col_to=%s, separator=%s",
                 len(file_sent),
                 clusters,
                 col_from,
                 col_to,
                 separator)

    if file_sent:
        try:
            ret = run_kmeans(csv_data, int(clusters), col_from, col_to, separator)
        except Exception as error:
            return create_error_response(400, "Failed running kmeans on provided input : %s" % error)
        else:
            return func.HttpResponse(ret.encode('utf-8'))
    else:
        logging.error("No data sent in request, returning code 400")
        return create_error_response(400, "Please pass valid content in the request body")


def run_kmeans(csv: str, clusters: int, col_from: str, col_to: str, separator: str) -> str:
    import time
    start = time.time_ns()

    df = pd.read_csv(StringIO(csv), sep=separator)

    # validating col_from and col_to. In case not set, initialize to 0:LAST_COLUMN
    if len(col_from) > 0:
        col_from = int(col_from)
    else:
        col_from = 0

    if len(col_to) > 0:
        col_to = int(col_to)
    else:
        col_to = len(df.columns) - 1

    if df.size < 1:
        raise Exception('Data Frame size is too small: %s')

    # x is the actual data set
    x = df.iloc[:, col_from:col_to].values

    # run kmeans algorithm
    kmeans = KMeans(n_clusters=clusters)
    y_kmeans = kmeans.fit_predict(x)

    end = time.time_ns()
    logging.info("Successfully performed kmeans, elapsed: %d ms", start, end, (end - start) / 1000000)

    return generate_output(df, y_kmeans, col_from, col_to, end-start)


def generate_output(df: pd.DataFrame, y_kmeans: np.ndarray, from_col: int, to_col: int, elapsed_time_ns: int) -> str:
    result = {}
    stats = {}
    clusters = {}
    result['stats'] = stats
    result['clusters'] = clusters

    for index in range(0, y_kmeans.size):
        cluster = int(y_kmeans[index])

        if cluster not in clusters.keys():
            curr_dict = {}
            clusters[cluster] = curr_dict
        curr_dict = clusters[cluster]
        curr_dict[index] = str(df.iloc[index, :].values.tolist()).strip('[]')

    stats['status'] = 'success'
    stats['took_time_ms'] = elapsed_time_ns / 1000000
    stats['total samples'] = df.shape[0]
    stats['total_columns'] = df.shape[1]
    stats['total_features'] = to_col - from_col
    stats['clustering_from_col'] = from_col
    stats['clustering_to_col'] = to_col

    return json.dumps(result, sort_keys=True)


def create_error_response(code: int, error: str) -> func.HttpResponse:
    json_dict = {
        'err_code': code,
        'error': error,
    }

    return func.HttpResponse(
        json.dumps(json_dict),
        status_code=code
    )
