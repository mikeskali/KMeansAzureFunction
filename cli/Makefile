#!/usr/bin/make -f
# ----------------------------------------------------------------------
#

docker-build:
	docker build -t kmeans-cli .

docker-run:
	docker run --network="host" -v $(shell pwd)/../SampleDataSets/iris.csv:/app/input/input.csv kmeans-cli python kmeans_cli.py http://host.docker.internal:7071/api/KMeansHttpTrigger /app/input/input.csv --clusters 3 --col_from 0 --col_to 4