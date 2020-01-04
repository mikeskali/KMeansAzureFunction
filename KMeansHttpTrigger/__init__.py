import logging

import azure.functions as func
import pandas as pd
from sklearn.cluster import KMeans
from io import StringIO


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # mandatory parameters
        file_sent = req.get_body()
        clusters = int(req.params.get('clusters'))
        csv_data = file_sent.decode("utf-8")
    except ValueError:
        logging.error("There was an error: %s",  ValueError)
        return func.HttpResponse(
            "There was an error: %s" % ValueError,
            status_code=400
        )

    # optional parameters
    col_from = req.params.get('col_from')
    col_to = req.params.get('col_to')
    separator = req.params.get('separator', ",")

    if file_sent:
        logging.info("Request data: data_size=%s, #of clusters=%s, col_from=%s, col_to=%s, separator=%s",
                     len(file_sent),
                     clusters,
                     col_from,
                     col_to,
                     separator)

        ret = run_kmeans(csv_data, int(clusters), col_from, col_to, separator)
        return func.HttpResponse(str(ret))
    else:
        logging.error("No data sent in request, returning code 400")
        return func.HttpResponse(
            "Please pass a file in the request body",
            status_code=400
        )


def run_kmeans(csv: str, clusters: int, col_from: str, col_to: str, separator: str) -> str:
    df = pd.read_csv(StringIO(csv), sep=separator)

    # validating col_from and col_to. In caes not set, initialize to 0:LAST_COLUMN
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

    x = df.iloc[:, col_from:col_to].values
    kmeans3 = KMeans(n_clusters=clusters)
    y_kmeans3 = kmeans3.fit_predict(x)

    return y_kmeans3


