# tests/test_httptrigger.py
import unittest
import json

import azure.functions as func
from KMeansHttpTrigger import main


class TestFunction(unittest.TestCase):
    def test_positive_flow(self):
        with open('../SampleDataSets/iris.csv', 'r') as reader:
            data = reader.read()
            req = func.HttpRequest(
                method='GET',
                body=data.encode('utf-8'),
                url='/api/KMeansHttpTrigger',
                params={'clusters': '3',
                        'col_from': '0',
                        'col_to': '3'
                        })

            # Call the function.
            resp = main(req)

            self.assertEqual(resp.status_code, 200, 'Received an error, this is unexpected')
            res = json.loads(resp.get_body())
            self.assertEqual(len(res['clusters'].keys()), 3, 'Expecting to get 3 clusters here')

    def test_bad_content(self):
        with open('test_kmeans_function.py', 'r') as reader:
            data = reader.read()
            req = func.HttpRequest(
                method='GET',
                body=data.encode('utf-8'),
                url='/api/KMeansHttpTrigger',
                params={'clusters': '3',
                        'col_from': '0',
                        'col_to': '3'
                        })

            # Call the function.
            resp = main(req)

            self.assertEqual(resp.status_code, 400, 'HTTP response code 400 was expected')
            res = json.loads(resp.get_body())
            self.assertTrue(len(res['error']) > 0, 'Should always have an error in case of failure ')

    def test_missing_clusters_param(self):
        with open('../SampleDataSets/iris.csv', 'r') as reader:
            data = reader.read()
            req = func.HttpRequest(
                method='GET',
                body=data.encode('utf-8'),
                url='/api/KMeansHttpTrigger',
                params={'col_from': '0',
                        'col_to': '3'
                        })

            # Call the function.
            resp = main(req)

            self.assertEqual(resp.status_code, 400, 'HTTP response code 400 was expected')
            res = json.loads(resp.get_body())
            self.assertTrue(len(res['error']) > 0, 'Should always have an error in case of failure ')