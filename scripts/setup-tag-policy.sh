#!/bin/bash

echo "Setting up Tag Policy for GenAI Pipeline Project..."

# Create tag policy (requires AWS Organizations)
aws organizations create-policy \
  --name "GenAIPipelineTagPolicy" \
  --description "Tag policy for GenAI pipeline resources" \
  --content file://../infra/policies/tag-policy.json \
  --type TAG_POLICY

echo "Tag policy created successfully!"