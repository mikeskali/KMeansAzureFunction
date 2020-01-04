import logging

import azure.functions as func
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from io import StringIO


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    file_sent = None

    try:
        file_sent = req.get_body()
    except ValueError:
        pass

    csv_data = file_sent.decode("utf-8")

    if file_sent:
        ret = run_kmeans(csv_data)
        return func.HttpResponse(str(ret))
    else:
        return func.HttpResponse(
            "Please pass a file in the request body",
            status_code=400
        )

def run_kmeans(csv) -> str:
    df = pd.read_csv(StringIO(csv), sep=",")

    x = df.iloc[:, [0, 1, 2, 3]].values
    kmeans3 = KMeans(n_clusters=3)
    y_kmeans3 = kmeans3.fit_predict(x)

    return y_kmeans3
    # # return df.head(10)
    # return len(csv)

def prepare_result(x, y_kmeans) -> str:

    # clusters_dict = {}
    # for index, row in x.iterrows():


