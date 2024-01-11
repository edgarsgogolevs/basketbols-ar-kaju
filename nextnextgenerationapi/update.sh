#!/bin/bash
source .azenv
az account set --subscription $SUBSCRIPTION
az containerapp up \
  --name $API_NAME \
  --resource-group $RESOURCE_GROUP \
  --source .
