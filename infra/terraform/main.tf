# Terraform configuration for GenAI pipeline with ARM64/Graviton optimization

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "project_name" {
  default = "GenAIPipeline"
}

variable "environment" {
  default = "dev"
}

variable "aws_region" {
  default = "us-east-1"
}

# Lambda functions with ARM64 architecture
resource "aws_lambda_function" "inference_arm64" {
  filename         = "genai-pipeline.zip"
  function_name    = "${var.project_name}-Inference-${var.environment}"
  role            = aws_iam_role.lambda_role.arn
  handler         = "inference.lambda_handler"
  runtime         = "python3.11"
  architectures   = ["arm64"]
  memory_size     = 1024
  timeout         = 300

  tags = {
    Project      = var.project_name
    Environment  = var.environment
    Architecture = "ARM64"
    Service      = "Graviton"
  }
}

# ECS with Graviton instances
resource "aws_ecs_cluster" "genai_cluster" {
  name = "${var.project_name}-cluster-${var.environment}"
  
  tags = {
    Project      = var.project_name
    Environment  = var.environment
    Architecture = "ARM64"
  }
}

resource "aws_ecs_task_definition" "genai_task" {
  family                   = "${var.project_name}-task"
  requires_compatibilities = ["EC2"]
  network_mode            = "bridge"
  cpu                     = "1024"
  memory                  = "2048"
  
  runtime_platform {
    cpu_architecture        = "ARM64"
    operating_system_family = "LINUX"
  }

  container_definitions = jsonencode([
    {
      name  = "genai-container"
      image = "public.ecr.aws/lambda/python:3.11-arm64"
      memory = 2048
      essential = true
    }
  ])

  tags = {
    Project      = var.project_name
    Environment  = var.environment
    Architecture = "ARM64"
  }
}

# IAM role for Lambda
resource "aws_iam_role" "lambda_role" {
  name = "${var.project_name}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.lambda_role.name
}

resource "aws_iam_role_policy" "bedrock_access" {
  name = "bedrock-access"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel",
          "bedrock:InvokeModelWithResponseStream"
        ]
        Resource = "*"
      }
    ]
  })
}