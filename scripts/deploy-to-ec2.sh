#!/bin/bash
# Deploy GenAI Pipeline to existing ARM64/Graviton EC2 instance

set -e

# Configuration
PUBLIC_IP=""
KEY_PAIR_NAME=""
PROJECT_DIR="/home/ubuntu/genai-pipeline"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_usage() {
    echo "Usage: $0 -i PUBLIC_IP -k KEY_PAIR_NAME"
    echo ""
    echo "Options:"
    echo "  -i PUBLIC_IP      Public IP address of EC2 instance"
    echo "  -k KEY_PAIR_NAME  EC2 Key Pair name (without .pem extension)"
    echo ""
    echo "Example:"
    echo "  $0 -i 54.123.45.67 -k my-key-pair"
}

# Parse command line arguments
while getopts "i:k:h" opt; do
    case $opt in
        i) PUBLIC_IP="$OPTARG" ;;
        k) KEY_PAIR_NAME="$OPTARG" ;;
        h) print_usage; exit 0 ;;
        *) print_usage; exit 1 ;;
    esac
done

# Validate required parameters
if [ -z "$PUBLIC_IP" ] || [ -z "$KEY_PAIR_NAME" ]; then
    echo -e "${RED}Error: Both public IP and key pair name are required${NC}"
    print_usage
    exit 1
fi

# Check if key file exists
if [ ! -f "${KEY_PAIR_NAME}.pem" ]; then
    echo -e "${RED}Error: Key file '${KEY_PAIR_NAME}.pem' not found${NC}"
    exit 1
fi

echo -e "${GREEN}🚀 Deploying GenAI Pipeline to ARM64/Graviton EC2${NC}"
echo "Target IP: $PUBLIC_IP"
echo "Key Pair: $KEY_PAIR_NAME"
echo ""

# Test SSH connection
echo -e "${YELLOW}🔗 Testing SSH connection...${NC}"
if ! ssh -i "${KEY_PAIR_NAME}.pem" -o ConnectTimeout=10 -o StrictHostKeyChecking=no ubuntu@"$PUBLIC_IP" "echo 'SSH connection successful'" > /dev/null 2>&1; then
    echo -e "${RED}❌ SSH connection failed. Check IP address and key pair.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ SSH connection successful${NC}"

# Update repository
echo -e "${YELLOW}📦 Updating repository on EC2...${NC}"
ssh -i "${KEY_PAIR_NAME}.pem" -o StrictHostKeyChecking=no ubuntu@"$PUBLIC_IP" << 'EOF'
cd /home/ubuntu/genai-pipeline
git pull origin main
pip3 install -r requirements.txt --upgrade
EOF

# Copy environment file if it exists locally
if [ -f ".env" ]; then
    echo -e "${YELLOW}📋 Copying environment configuration...${NC}"
    scp -i "${KEY_PAIR_NAME}.pem" -o StrictHostKeyChecking=no .env ubuntu@"$PUBLIC_IP":/home/ubuntu/genai-pipeline/
fi

# Build ARM64 Docker image on EC2
echo -e "${YELLOW}🐳 Building ARM64 Docker image...${NC}"
ssh -i "${KEY_PAIR_NAME}.pem" -o StrictHostKeyChecking=no ubuntu@"$PUBLIC_IP" << 'EOF'
cd /home/ubuntu/genai-pipeline
if [ -f "Dockerfile.arm64" ]; then
    sudo docker build -f Dockerfile.arm64 -t genai-pipeline:arm64 .
    echo "✅ Docker image built successfully"
else
    echo "⚠️  Dockerfile.arm64 not found, skipping Docker build"
fi
EOF

# Start/restart the service
echo -e "${YELLOW}🔄 Starting GenAI Pipeline service...${NC}"
ssh -i "${KEY_PAIR_NAME}.pem" -o StrictHostKeyChecking=no ubuntu@"$PUBLIC_IP" << 'EOF'
# Check if AWS credentials are configured
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo "⚠️  AWS credentials not configured. Please run: aws configure"
    echo "   You can do this by running: ssh -i your-key.pem ubuntu@your-ip"
    echo "   Then: aws configure"
else
    # Restart the service
    sudo systemctl restart genai-pipeline
    sleep 5
    
    # Check service status
    if sudo systemctl is-active --quiet genai-pipeline; then
        echo "✅ GenAI Pipeline service is running"
        
        # Test the API
        sleep 10
        if curl -s http://localhost:8000/health > /dev/null; then
            echo "✅ API health check passed"
        else
            echo "⚠️  API health check failed"
        fi
    else
        echo "❌ GenAI Pipeline service failed to start"
        sudo systemctl status genai-pipeline --no-pager
    fi
fi
EOF

echo ""
echo -e "${GREEN}🎉 Deployment completed!${NC}"
echo ""
echo -e "${YELLOW}📝 Next Steps:${NC}"
echo "1. If AWS credentials aren't configured, SSH to the instance:"
echo "   ssh -i ${KEY_PAIR_NAME}.pem ubuntu@$PUBLIC_IP"
echo "   aws configure"
echo ""
echo "2. Test the API:"
echo "   curl http://$PUBLIC_IP:8000/health"
echo ""
echo "3. Send inference request:"
echo "   curl -X POST http://$PUBLIC_IP:8000/ \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"prompt\": \"What is AI?\"}'"
echo ""
echo "4. Monitor logs:"
echo "   ssh -i ${KEY_PAIR_NAME}.pem ubuntu@$PUBLIC_IP"
echo "   sudo journalctl -u genai-pipeline -f"