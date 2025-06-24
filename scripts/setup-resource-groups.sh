#!/bin/bash

echo "Setting up Resource Groups for GenAI Pipeline Project..."

# Create main resource group for all project resources
aws resource-groups create-group \
  --name "GenAIPipeline-All" \
  --description "All resources for GenAI pipeline project" \
  --resource-query '{"Type":"TAG_FILTERS_1_0","Query":"{\"ResourceTypeFilters\":[\"AWS::AllSupported\"],\"TagFilters\":[{\"Key\":\"Project\",\"Values\":[\"GenAIPipeline\"]}]}"}'

# Create resource group for development environment
aws resource-groups create-group \
  --name "GenAIPipeline-Dev" \
  --description "Development resources for GenAI pipeline project" \
  --resource-query '{"Type":"TAG_FILTERS_1_0","Query":"{\"ResourceTypeFilters\":[\"AWS::AllSupported\"],\"TagFilters\":[{\"Key\":\"Project\",\"Values\":[\"GenAIPipeline\"]},{\"Key\":\"Environment\",\"Values\":[\"dev\"]}]}"}'

# Create resource group for production environment
aws resource-groups create-group \
  --name "GenAIPipeline-Prod" \
  --description "Production resources for GenAI pipeline project" \
  --resource-query '{"Type":"TAG_FILTERS_1_0","Query":"{\"ResourceTypeFilters\":[\"AWS::AllSupported\"],\"TagFilters\":[{\"Key\":\"Project\",\"Values\":[\"GenAIPipeline\"]},{\"Key\":\"Environment\",\"Values\":[\"prod\"]}]}"}'

# Create resource group for model inference component
aws resource-groups create-group \
  --name "GenAIPipeline-Inference" \
  --description "Model inference resources for GenAI pipeline project" \
  --resource-query '{"Type":"TAG_FILTERS_1_0","Query":"{\"ResourceTypeFilters\":[\"AWS::AllSupported\"],\"TagFilters\":[{\"Key\":\"Project\",\"Values\":[\"GenAIPipeline\"]},{\"Key\":\"Component\",\"Values\":[\"ModelInference\"]}]}"}'

echo "Resource groups created successfully!"
echo "Listing all resource groups:"
aws resource-groups list-groups --query 'GroupList[?contains(Name, `GenAIPipeline`)].Name' --output table