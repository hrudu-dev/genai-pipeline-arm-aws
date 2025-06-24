#!/bin/bash
# User Data Script for GenAI Pipeline ARM64/Graviton EC2

set -e

# Update system
apt-get update
apt-get upgrade -y

# Install essential packages
apt-get install -y \
    docker.io \
    git \
    python3-pip \
    awscli \
    htop \
    curl \
    wget \
    unzip

# Start and enable Docker
systemctl start docker
systemctl enable docker
usermod -aG docker ubuntu

# Install Docker Compose for ARM64
curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-linux-aarch64" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Clone GenAI Pipeline repository
cd /home/ubuntu
git clone https://github.com/hrudu-dev/genai-pipeline.git
chown -R ubuntu:ubuntu genai-pipeline

# Install Python dependencies
cd genai-pipeline
pip3 install -r requirements.txt

# Create environment file template
cat > .env << EOF
AWS_DEFAULT_REGION=us-east-1
AWS_REGION=us-east-1
PROJECT_NAME=${project_name}
ENVIRONMENT=production
EOF

chown ubuntu:ubuntu .env

# Create systemd service for GenAI Pipeline
cat > /etc/systemd/system/genai-pipeline.service << EOF
[Unit]
Description=GenAI Pipeline Service
After=network.target docker.service
Requires=docker.service

[Service]
Type=simple
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/genai-pipeline
Environment=PATH=/usr/local/bin:/usr/bin:/bin
ExecStart=/usr/bin/python3 -m uvicorn src.inference:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable but don't start the service (requires AWS credentials)
systemctl daemon-reload
systemctl enable genai-pipeline

# Install CloudWatch agent
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/arm64/latest/amazon-cloudwatch-agent.deb
dpkg -i amazon-cloudwatch-agent.deb

# Create log directory
mkdir -p /var/log/genai-pipeline
chown ubuntu:ubuntu /var/log/genai-pipeline

# Create startup script
cat > /home/ubuntu/start-pipeline.sh << 'EOF'
#!/bin/bash
echo "Starting GenAI Pipeline..."
cd /home/ubuntu/genai-pipeline

# Check if AWS credentials are configured
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo "AWS credentials not configured. Please run: aws configure"
    exit 1
fi

# Start the service
sudo systemctl start genai-pipeline
sudo systemctl status genai-pipeline

echo "GenAI Pipeline started on port 8000"
echo "Access at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8000"
EOF

chmod +x /home/ubuntu/start-pipeline.sh
chown ubuntu:ubuntu /home/ubuntu/start-pipeline.sh

# Create welcome message
cat > /etc/motd << EOF

🚀 GenAI Pipeline ARM64/Graviton EC2 Instance

Instance Type: $(curl -s http://169.254.169.254/latest/meta-data/instance-type)
Architecture: ARM64 (Graviton)
Project: ${project_name}

Quick Start:
1. Configure AWS credentials: aws configure
2. Start pipeline: ./start-pipeline.sh
3. Test API: curl http://localhost:8000/health

Documentation: /home/ubuntu/genai-pipeline/README.md

EOF

echo "✅ GenAI Pipeline ARM64 EC2 setup complete!"