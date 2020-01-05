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
        json = r.json()

        if r.status_code != 200:
            logger.info("Clustering failed. Status code: %s. Error: %s", json['err_code'], json['error'])
            return

        logger.info("============ stats ==============")
        for key in json['stats']:
            logger.info("  %s:%s", key, json['stats'][key])

        logger.info("")
        logger.info("======================== Clusters =======================")
        logger.info("sample number: sample coordinates")

        for cluster_id in json['clusters']:
            logger.info("====== Cluster %s =======", cluster_id)
            cluster = json['clusters'][cluster_id]
            for key in cluster:
                logger.info(" %s: %s", key, cluster[key])

if __name__ == '__main__':
    fire.Fire(kmeans)
