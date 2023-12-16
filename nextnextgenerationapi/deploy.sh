#!/bin/bash
source .azenv

# Build and push image to Azure Container Registry
az acr build \
  --registry $ACR_NAME \
  --image $API_NAME:latest \
  --file Dockerfile .

az containerapp up \
  --name $API_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $ENVIRONMENT \
  --image $ACR_NAME.azurecr.io/$API_NAME:latest \
  --target-port $PORT \
  --env-vars $AZURE_ENV_VARS \
  --ingress 'external' \
  --registry-server $ACR_NAME.azurecr.io \
  --cpu 2 \
  --memory 4 \
  --scale 3 \
  --query properties.configuration.ingress.fqdn 
