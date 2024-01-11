#!/bin/bash
source .azenv

# npm install
npm run build

az account set --subscription $SUBSCRIPTION

az containerapp up \
  --name $FRONTEND_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $ENVIRONMENT \
  --registry-server $ACR_NAME.azurecr.io \
  --source .
