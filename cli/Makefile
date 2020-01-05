#!/usr/bin/make -f
# ----------------------------------------------------------------------
#

docker-build:
	docker build -t kmeans-cli .

docker-run-request:
	docker run --network="host" -v $(shell pwd)/../SampleDataSets/iris.csv:/app/input/input.csv kmeans-cli python kmeans_cli.py http://host.docker.internal:7071/api/KMeansHttpTrigger /app/input/input.csv --clusters 3 --col_from 0 --col_to 4

run-cli-request:
	python kmeans_cli.py http://localhost:7071/api/KMeansHttpTrigger ../SampleDataSets/iris.csv --clusters 3 --col_from 0 --col_to 4
