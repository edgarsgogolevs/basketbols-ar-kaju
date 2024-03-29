#!/bin/bash
source .azenv

# npm install
npm run build

az account set --subscription $SUBSCRIPTION

az containerapp up \
  --name $FRONTEND_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $ENVIRONMENT \
  --source . \
  --target-port $PORT \
  --env-vars $AZURE_ENV_VARS \
  --ingress 'external' \
  --registry-server $ACR_NAME.azurecr.io \
  --cpu 1 \
  --memory 2 \
  --query properties.configuration.ingress.fqdn 
