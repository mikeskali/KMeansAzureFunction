#!/usr/bin/make -f
# ----------------------------------------------------------------------
#

run-locally:
	func host start

deploy-to-azure:
	func azure functionapp publish KMeansAzureFunction

send-sample-request:
	curl --data-binary "@SampleDataSets/iris.csv" 'http://localhost:7071/api/KMeansHttpTrigger?clusters=3&col_from=0&col_to=3&separator=,'