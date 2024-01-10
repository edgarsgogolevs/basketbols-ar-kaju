#!/bin/bash
source .azenv

az account set --subscription $SUBSCRIPTION

# Build and push image to Azure Container Registry
az acr build \
  --registry $ACR_NAME \
  --image $API_NAME:latest \
  --file Dockerfile .

az containerapp up \
  --name $API_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $ENVIRONMENT \
  --image $ACR_NAME.azurecr.io/${API_NAME}:latest \
  --target-port $PORT \
  --env-vars $AZURE_ENV_VARS \
  --ingress 'external' \
  --registry-server $ACR_NAME.azurecr.io \
  --query properties.configuration.ingress.fqdn 


# az containerapp create \
#   --name $API_NAME \
#   --resource-group $RESOURCE_GROUP \
#   --environment $ENVIRONMENT \
#   --image $ACR_NAME.azurecr.io/$API_NAME:latest \
#   --target-port $PORT \
#   --env-vars $AZURE_ENV_VARS \
#   --ingress 'external' \
#   --registry-server $ACR_NAME.azurecr.io \
#   --cpu 0.5 \
#   --memory 1 \
#   --min-instances 1 \
#   --max-instances 5 \
#   --query properties.configuration.ingress.fqdn 
