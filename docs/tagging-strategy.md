# GenAI Pipeline Tagging Strategy

## Tag Standards

| Tag Key | Description | Example Values |
|---------|-------------|----------------|
| Project | Project identifier | GenAIPipeline |
| Environment | Deployment environment | dev, test, prod |
| Component | Pipeline component | DataProcessing, ModelInference, Orchestration |
| Service | AWS service | Bedrock, Graviton, AmazonQ |
| CostCenter | Financial tracking | ML-12345 |
| Owner | Team responsible | AITeam |

## Resource Groups

- **GenAIPipeline-All**: All project resources
- **GenAIPipeline-Dev**: Development environment resources
- **GenAIPipeline-Prod**: Production environment resources
- **GenAIPipeline-Inference**: Model inference components

## Getting Started

### Quick Setup (CLI)
```bash
# Set up resource groups
./scripts/setup-resource-groups.sh

# Set up tag policy (requires AWS Organizations)
./scripts/setup-tag-policy.sh

# Tag existing resources
./scripts/tag_resources.sh
```

### CloudFormation Deployment
```bash
# Deploy tagging infrastructure
./scripts/deploy-tagging-stack.sh
```

## Best Practices

1. **Tag at creation time** - Easier than retroactive tagging
2. **Be consistent** - Use standardized tag keys and values
3. **Automate tagging** - Use AWS Config rules for enforcement
4. **Document strategy** - Keep this guide updated
5. **Monitor compliance** - Regular audits of tagging