# Security Policy

## Supported Versions

We actively support the following versions of the GenAI Pipeline:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Security Features

### 🔐 Built-in Security Measures

- **Environment Variable Protection**: All sensitive credentials stored in `.env` files (never committed)
- **IAM Role-based Access**: Least privilege access using AWS IAM roles
- **HTTPS Only**: All API communications use TLS encryption
- **Input Validation**: Prompt sanitization and validation
- **Error Handling**: Secure error messages without sensitive data exposure
- **CORS Configuration**: Properly configured cross-origin resource sharing

### 🛡️ AWS Security Integration

- **AWS Bedrock**: Secure model inference with built-in AWS security
- **Lambda Function URLs**: Secure serverless endpoints
- **CloudWatch Logging**: Comprehensive audit trails
- **VPC Support**: Optional VPC deployment for enhanced isolation

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue, please follow these steps:

### 📧 Contact Information

- **Email**: [security@yourproject.com] (replace with actual email)
- **Response Time**: We aim to respond within 24 hours
- **Resolution Time**: Critical issues resolved within 72 hours

### 🔍 What to Include

When reporting a vulnerability, please include:

1. **Description**: Clear description of the vulnerability
2. **Steps to Reproduce**: Detailed steps to reproduce the issue
3. **Impact Assessment**: Potential impact and affected components
4. **Suggested Fix**: If you have suggestions for remediation
5. **Contact Information**: How we can reach you for follow-up

### 📋 Vulnerability Assessment Process

1. **Initial Response** (24 hours): Acknowledgment of report
2. **Investigation** (48 hours): Technical assessment and validation
3. **Resolution** (72 hours): Fix development and testing
4. **Disclosure** (7 days): Coordinated disclosure after fix deployment

## Security Best Practices

### 🔧 For Developers

```bash
# Always use environment variables for credentials
AWS_ACCESS_KEY_ID=your_key_here
AWS_SECRET_ACCESS_KEY=your_secret_here

# Never commit sensitive files
echo ".env" >> .gitignore
echo "*.pem" >> .gitignore
echo "credentials.json" >> .gitignore
```

### 🏗️ For Deployment

```bash
# Use IAM roles instead of access keys when possible
# Enable CloudTrail for audit logging
# Regularly rotate access keys
# Use least privilege IAM policies
```

### 🌐 For API Usage

```python
# Always validate input
def validate_prompt(prompt):
    if not prompt or len(prompt) > 1000:
        raise ValueError("Invalid prompt")
    return prompt.strip()

# Use timeout for external calls
response = requests.post(url, json=data, timeout=30)
```

## Security Configuration

### 🔐 Environment Variables

Required security-related environment variables:

```bash
# AWS Credentials (use IAM roles in production)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1

# Lambda Configuration
LAMBDA_ROLE_ARN=arn:aws:iam::ACCOUNT:role/lambda-bedrock-role
```

### 🛡️ IAM Policy Template

Minimal IAM policy for the Lambda function:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel"
            ],
            "Resource": [
                "arn:aws:bedrock:*:*:model/anthropic.claude-3-haiku-20240307-v1:0"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        }
    ]
}
```

## Security Checklist

### ✅ Before Deployment

- [ ] Environment variables configured
- [ ] IAM roles and policies reviewed
- [ ] Secrets not in code repository
- [ ] HTTPS endpoints configured
- [ ] Input validation implemented
- [ ] Error handling reviewed
- [ ] Logging configured
- [ ] Access controls tested

### ✅ Regular Maintenance

- [ ] Dependencies updated monthly
- [ ] Security patches applied
- [ ] Access keys rotated quarterly
- [ ] IAM policies reviewed
- [ ] Logs monitored for anomalies
- [ ] Vulnerability scans performed

## Known Security Considerations

### 🚨 Current Limitations

1. **Function URL Public Access**: Lambda Function URLs are publicly accessible
   - **Mitigation**: Implement API key authentication if needed
   - **Alternative**: Use API Gateway with authentication

2. **Input Size Limits**: Large prompts could cause resource exhaustion
   - **Mitigation**: Input validation and size limits implemented
   - **Monitoring**: CloudWatch metrics for request sizes

3. **Rate Limiting**: No built-in rate limiting on Function URLs
   - **Mitigation**: Consider API Gateway for production use
   - **Monitoring**: CloudWatch alarms for unusual traffic

### 🔄 Planned Security Enhancements

- [ ] API key authentication
- [ ] Request rate limiting
- [ ] Enhanced input sanitization
- [ ] Security headers implementation
- [ ] Automated security scanning

## Compliance

### 📋 Standards Alignment

- **AWS Well-Architected Framework**: Security pillar compliance
- **OWASP Top 10**: Protection against common vulnerabilities
- **SOC 2**: AWS infrastructure compliance
- **GDPR**: Data processing transparency (no PII stored)

### 🔍 Security Monitoring

- **CloudWatch**: Real-time monitoring and alerting
- **CloudTrail**: API call auditing
- **AWS Config**: Configuration compliance
- **AWS Security Hub**: Centralized security findings

## Contact

For security-related questions or concerns:

- **Project Maintainer**: [Your Name]
- **Security Team**: [security@yourproject.com]
- **GitHub Issues**: Use for non-sensitive security discussions

---

**Last Updated**: January 2025
**Next Review**: April 2025