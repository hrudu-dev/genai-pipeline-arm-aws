#!/bin/bash
# Launch ARM64/Graviton EC2 instance for GenAI Pipeline

set -e

# Configuration
PROJECT_NAME="GenAIPipeline"
ENVIRONMENT="dev"
INSTANCE_TYPE="t4g.medium"
KEY_PAIR_NAME=""
STACK_NAME="${PROJECT_NAME}-EC2-ARM64-${ENVIRONMENT}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_usage() {
    echo "Usage: $0 -k KEY_PAIR_NAME [-t INSTANCE_TYPE] [-e ENVIRONMENT]"
    echo ""
    echo "Options:"
    echo "  -k KEY_PAIR_NAME    EC2 Key Pair name (required)"
    echo "  -t INSTANCE_TYPE    Instance type (default: t4g.medium)"
    echo "  -e ENVIRONMENT      Environment (default: dev)"
    echo ""
    echo "Supported instance types:"
    echo "  t4g.micro    - 2 vCPU, 1 GB RAM   (~$6/month)"
    echo "  t4g.small    - 2 vCPU, 2 GB RAM   (~$12/month)"
    echo "  t4g.medium   - 2 vCPU, 4 GB RAM   (~$24/month)"
    echo "  c7g.large    - 2 vCPU, 4 GB RAM   (~$50/month, compute optimized)"
    echo "  m7g.xlarge   - 4 vCPU, 16 GB RAM  (~$120/month, general purpose)"
}

# Parse command line arguments
while getopts "k:t:e:h" opt; do
    case $opt in
        k) KEY_PAIR_NAME="$OPTARG" ;;
        t) INSTANCE_TYPE="$OPTARG" ;;
        e) ENVIRONMENT="$OPTARG" ;;
        h) print_usage; exit 0 ;;
        *) print_usage; exit 1 ;;
    esac
done

# Validate required parameters
if [ -z "$KEY_PAIR_NAME" ]; then
    echo -e "${RED}Error: Key pair name is required${NC}"
    print_usage
    exit 1
fi

echo -e "${GREEN}🚀 Launching GenAI Pipeline ARM64/Graviton EC2 Instance${NC}"
echo "Project: $PROJECT_NAME"
echo "Environment: $ENVIRONMENT"
echo "Instance Type: $INSTANCE_TYPE"
echo "Key Pair: $KEY_PAIR_NAME"
echo "Stack Name: $STACK_NAME"
echo ""

# Check if AWS CLI is configured
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo -e "${RED}Error: AWS CLI not configured. Run 'aws configure' first.${NC}"
    exit 1
fi

# Check if key pair exists
if ! aws ec2 describe-key-pairs --key-names "$KEY_PAIR_NAME" > /dev/null 2>&1; then
    echo -e "${RED}Error: Key pair '$KEY_PAIR_NAME' not found${NC}"
    echo "Create a key pair first: aws ec2 create-key-pair --key-name $KEY_PAIR_NAME --query 'KeyMaterial' --output text > $KEY_PAIR_NAME.pem"
    exit 1
fi

# Deploy CloudFormation stack
echo -e "${YELLOW}📦 Deploying CloudFormation stack...${NC}"
aws cloudformation deploy \
    --template-file infra/cloudformation/ec2-arm64.yaml \
    --stack-name "$STACK_NAME" \
    --parameter-overrides \
        ProjectName="$PROJECT_NAME" \
        Environment="$ENVIRONMENT" \
        InstanceType="$INSTANCE_TYPE" \
        KeyPairName="$KEY_PAIR_NAME" \
    --capabilities CAPABILITY_IAM \
    --tags \
        Project="$PROJECT_NAME" \
        Environment="$ENVIRONMENT" \
        Architecture="ARM64" \
        Service="Graviton"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ CloudFormation stack deployed successfully${NC}"
else
    echo -e "${RED}❌ CloudFormation deployment failed${NC}"
    exit 1
fi

# Get instance details
echo -e "${YELLOW}📋 Getting instance details...${NC}"
INSTANCE_ID=$(aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --query 'Stacks[0].Outputs[?OutputKey==`InstanceId`].OutputValue' \
    --output text)

PUBLIC_IP=$(aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --query 'Stacks[0].Outputs[?OutputKey==`PublicIP`].OutputValue' \
    --output text)

echo ""
echo -e "${GREEN}🎉 EC2 Instance launched successfully!${NC}"
echo ""
echo "Instance ID: $INSTANCE_ID"
echo "Public IP: $PUBLIC_IP"
echo "Instance Type: $INSTANCE_TYPE (ARM64/Graviton)"
echo ""
echo -e "${YELLOW}📝 Next Steps:${NC}"
echo "1. Wait for instance to finish bootstrapping (~3-5 minutes)"
echo "2. Connect via SSH:"
echo "   ssh -i $KEY_PAIR_NAME.pem ubuntu@$PUBLIC_IP"
echo ""
echo "3. Configure AWS credentials on the instance:"
echo "   aws configure"
echo ""
echo "4. Start the GenAI Pipeline:"
echo "   ./start-pipeline.sh"
echo ""
echo "5. Test the API:"
echo "   curl http://$PUBLIC_IP:8000/health"
echo ""
echo -e "${GREEN}💰 Estimated monthly cost: ~\$$(echo "scale=0; $INSTANCE_TYPE" | sed 's/t4g.micro/6/; s/t4g.small/12/; s/t4g.medium/24/; s/c7g.large/50/; s/m7g.xlarge/120/' | bc 2>/dev/null || echo "24")${NC}"