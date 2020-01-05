import logging
import fire
import requests


FORMAT = '%(message)s'
logging.basicConfig(format=FORMAT)
LOGGER = logging.getLogger('cli')
LOGGER.setLevel(level='INFO')


def kmeans(service_url: str, data_path: str, clusters: int, separator=",", col_from=0, col_to=0):
    LOGGER.info("""=========== Preparing to run KMeans==========
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
            LOGGER.info("Clustering failed. Status code: %s. Error: %s", json['err_code'], json['error'])
            return

        LOGGER.info("============ stats ==============")
        for key in json['stats']:
            LOGGER.info("  %s:%s", key, json['stats'][key])

        LOGGER.info("")
        LOGGER.info("======================== Clusters =======================")
        LOGGER.info("sample number: sample row")

        for cluster_id in json['clusters']:
            cluster = json['clusters'][cluster_id]
            LOGGER.info("")
            LOGGER.info("====== Cluster %s (%d members) =======", cluster_id, len(cluster.keys()))

            for key in cluster:
                LOGGER.info(" %s: %s", key, cluster[key])


if __name__ == '__main__':
    fire.Fire(kmeans)
