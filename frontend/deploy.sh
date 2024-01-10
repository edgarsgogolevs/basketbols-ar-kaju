#!/bin/bash
source .azenv

# npm install
# npm run build

az account set --subscription $SUBSCRIPTION

# Build and push image to Azure Container Registry
# az acr build \
#   --registry $ACR_NAME \
#   --image $FRONTEND_NAME:latest \
#   --file Dockerfile .

# Create container app
az containerapp create \
  --name $FRONTEND_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $ENVIRONMENT \
  --image $ACR_NAME.azurecr.io/$FRONTEND_NAME:latest \
  --target-port $PORT \
  --env-vars $AZURE_ENV_VARS \
  --ingress 'external' \
  --registry-server $ACR_NAME.azurecr.io \
  --cpu 1 \
  --memory 2 \
  --query properties.configuration.ingress.fqdn 
