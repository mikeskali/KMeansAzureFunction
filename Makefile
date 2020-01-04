#!/usr/bin/make -f
# ----------------------------------------------------------------------
#

run-locally:
	func host start

deploy-to-azure:
	func azure functionapp publish KMeansAzureFunction
