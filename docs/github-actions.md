# GitHub Actions Workflows

This document describes the GitHub Actions workflows used for CI/CD and maintenance of the GenAI Pipeline project.

## CI Workflow

**File:** `.github/workflows/ci.yml`

The CI workflow runs on every push to the main branch and on pull requests. It also runs weekly on Sunday at midnight.

### Jobs:

- **build-and-test**: Builds the project and runs tests on multiple Python versions.
  - Sets up Python (3.9 and 3.11)
  - Installs dependencies
  - Runs tests
  - Checks code quality with flake8

## Deploy Workflow

**File:** `.github/workflows/deploy.yml`

The deploy workflow runs on every push to the main branch (excluding documentation changes) and can be manually triggered.

### Jobs:

- **test**: Runs tests to ensure everything is working before deployment.
- **deploy-lambda**: Deploys the Lambda function to AWS.
  - Runs after the test job
  - Deploys to the specified environment (dev, staging, or prod)
  - Verifies the deployment by running a test
- **deploy-cache**: Sets up caching for the Lambda function.
  - Runs after the deploy-lambda job
  - Creates a DynamoDB table for caching
  - Deploys a cached version of the Lambda function
- **deploy-multi-region**: Deploys the Lambda function to multiple regions.
  - Only runs when manually triggered with the deploy_multi_region option

## Maintenance Workflow

**File:** `.github/workflows/maintenance.yml`

The maintenance workflow runs weekly on Monday at midnight and can be manually triggered.

### Jobs:

- **dependency-updates**: Checks for dependency updates and creates a pull request if updates are available.
  - Uses pip-tools to check for updates
  - Creates a pull request with the updated dependencies
- **security-scan**: Runs security scans on the codebase.
  - Uses Bandit to scan for security issues in the code
  - Uses Safety to check for vulnerable dependencies
- **cleanup-old-resources**: Cleans up old AWS resources.
  - Deletes Lambda functions older than 30 days
  - Deletes CloudWatch log groups older than 30 days
  - Deletes DynamoDB tables older than 30 days

## Documentation Workflow

**File:** `.github/workflows/docs.yml`

The documentation workflow runs on every push to the main branch that changes documentation files and can be manually triggered.

### Jobs:

- **update-docs**: Builds and deploys the documentation to GitHub Pages.
  - Uses MkDocs to build the documentation
  - Deploys the documentation to the gh-pages branch

## Workflow Triggers

| Workflow | Push to Main | Pull Request | Schedule | Manual |
|----------|-------------|--------------|----------|--------|
| CI | ✅ | ✅ | Weekly (Sunday) | ❌ |
| Deploy | ✅ (non-docs) | ❌ | ❌ | ✅ |
| Maintenance | ❌ | ❌ | Weekly (Monday) | ✅ |
| Documentation | ✅ (docs only) | ❌ | ❌ | ✅ |

## Environment Variables and Secrets

The workflows use the following environment variables and secrets:

- **AWS_ACCESS_KEY_ID**: AWS access key ID for authentication
- **AWS_SECRET_ACCESS_KEY**: AWS secret access key for authentication
- **AWS_DEFAULT_REGION**: AWS region to deploy to (default: us-east-1)
- **LAMBDA_ROLE_ARN**: ARN of the IAM role for the Lambda function
- **ENVIRONMENT**: Deployment environment (dev, staging, or prod)

## Manual Workflow Dispatch

The deploy and maintenance workflows can be manually triggered from the GitHub Actions tab. The deploy workflow allows you to select the environment and whether to deploy to multiple regions.

## Adding New Workflows

To add a new workflow:

1. Create a new YAML file in the `.github/workflows` directory
2. Define the workflow name, triggers, and jobs
3. Commit and push the file to the repository

## Troubleshooting

If a workflow fails:

1. Check the workflow logs in the GitHub Actions tab
2. Verify that all required secrets are set
3. Check that the AWS credentials have the necessary permissions
4. Ensure that the code passes all tests locally before pushing