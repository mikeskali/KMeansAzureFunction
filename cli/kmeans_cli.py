import fire
import logging
import requests


FORMAT = '%(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('cli')
logger.setLevel(level='INFO')

def kmeans(service_url: str, data_path: str, clusters: int, separator=",", col_from=0, col_to=0):
    logger.info("""Preparing to run KMeans.
        Service URL: %s
        Data path: %s
        clusters: %d
        separator: %s
        col_from: %d
        col_to: %d
        """,
        service_url, data_path, clusters, separator, col_from, col_to)

    PARAMS = {'clusters': clusters,
              'separator': separator,
              'col_from': col_from,
              'col_to': col_to
              }
    with open(data_path, 'r') as reader:
        data = reader.read()
        r = requests.post(url=service_url, params=PARAMS, data=data.encode('utf-8'))
        logger.info('got: %s, status code: %s', r.text, r.status_code)


if __name__ == '__main__':
    fire.Fire(kmeans)
