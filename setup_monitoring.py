#!/usr/bin/env python3
"""
Set up CloudWatch monitoring for GenAI Pipeline
"""

import boto3
import json

# Hardcoded credentials - only for testing
AWS_ACCESS_KEY_ID = "AKIAQCJFIBGQKP7OBYFN"
AWS_SECRET_ACCESS_KEY = "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"
AWS_DEFAULT_REGION = "us-east-1"

# Lambda function name
LAMBDA_FUNCTION_NAME = "GenAIPipelineTest2"

def setup_cloudwatch_dashboard():
    """Set up CloudWatch dashboard for Lambda function"""
    print("Setting up CloudWatch dashboard...")
    
    # Create CloudWatch client
    cloudwatch = boto3.client('cloudwatch',
                            region_name=AWS_DEFAULT_REGION,
                            aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    
    # Dashboard name
    dashboard_name = "GenAIPipelineDashboard"
    
    # Dashboard body
    dashboard_body = {
        "widgets": [
            {
                "type": "metric",
                "x": 0,
                "y": 0,
                "width": 12,
                "height": 6,
                "properties": {
                    "metrics": [
                        ["AWS/Lambda", "Invocations", "FunctionName", LAMBDA_FUNCTION_NAME, {"stat": "Sum"}]
                    ],
                    "view": "timeSeries",
                    "stacked": False,
                    "region": AWS_DEFAULT_REGION,
                    "title": "Lambda Invocations",
                    "period": 300
                }
            },
            {
                "type": "metric",
                "x": 12,
                "y": 0,
                "width": 12,
                "height": 6,
                "properties": {
                    "metrics": [
                        ["AWS/Lambda", "Duration", "FunctionName", LAMBDA_FUNCTION_NAME, {"stat": "Average"}],
                        ["AWS/Lambda", "Duration", "FunctionName", LAMBDA_FUNCTION_NAME, {"stat": "Maximum"}]
                    ],
                    "view": "timeSeries",
                    "stacked": False,
                    "region": AWS_DEFAULT_REGION,
                    "title": "Lambda Duration",
                    "period": 300
                }
            },
            {
                "type": "metric",
                "x": 0,
                "y": 6,
                "width": 12,
                "height": 6,
                "properties": {
                    "metrics": [
                        ["AWS/Lambda", "Errors", "FunctionName", LAMBDA_FUNCTION_NAME, {"stat": "Sum"}]
                    ],
                    "view": "timeSeries",
                    "stacked": False,
                    "region": AWS_DEFAULT_REGION,
                    "title": "Lambda Errors",
                    "period": 300
                }
            },
            {
                "type": "metric",
                "x": 12,
                "y": 6,
                "width": 12,
                "height": 6,
                "properties": {
                    "metrics": [
                        ["AWS/Lambda", "ConcurrentExecutions", "FunctionName", LAMBDA_FUNCTION_NAME, {"stat": "Maximum"}]
                    ],
                    "view": "timeSeries",
                    "stacked": False,
                    "region": AWS_DEFAULT_REGION,
                    "title": "Lambda Concurrent Executions",
                    "period": 300
                }
            }
        ]
    }
    
    # Create or update dashboard
    response = cloudwatch.put_dashboard(
        DashboardName=dashboard_name,
        DashboardBody=json.dumps(dashboard_body)
    )
    
    print(f"Dashboard created: {dashboard_name}")
    print(f"Dashboard URL: https://{AWS_DEFAULT_REGION}.console.aws.amazon.com/cloudwatch/home?region={AWS_DEFAULT_REGION}#dashboards:name={dashboard_name}")
    
    # Create alarms
    create_alarms(cloudwatch)
    
    return dashboard_name

def create_alarms(cloudwatch):
    """Create CloudWatch alarms for Lambda function"""
    print("Creating CloudWatch alarms...")
    
    # Error rate alarm
    cloudwatch.put_metric_alarm(
        AlarmName=f"{LAMBDA_FUNCTION_NAME}-ErrorAlarm",
        ComparisonOperator="GreaterThanThreshold",
        EvaluationPeriods=1,
        MetricName="Errors",
        Namespace="AWS/Lambda",
        Period=60,
        Statistic="Sum",
        Threshold=1,
        ActionsEnabled=False,
        AlarmDescription=f"Alarm when {LAMBDA_FUNCTION_NAME} has errors",
        Dimensions=[
            {
                "Name": "FunctionName",
                "Value": LAMBDA_FUNCTION_NAME
            }
        ]
    )
    
    # Duration alarm
    cloudwatch.put_metric_alarm(
        AlarmName=f"{LAMBDA_FUNCTION_NAME}-DurationAlarm",
        ComparisonOperator="GreaterThanThreshold",
        EvaluationPeriods=1,
        MetricName="Duration",
        Namespace="AWS/Lambda",
        Period=60,
        Statistic="Maximum",
        Threshold=5000,  # 5 seconds
        ActionsEnabled=False,
        AlarmDescription=f"Alarm when {LAMBDA_FUNCTION_NAME} duration exceeds 5 seconds",
        Dimensions=[
            {
                "Name": "FunctionName",
                "Value": LAMBDA_FUNCTION_NAME
            }
        ]
    )
    
    print("Alarms created")

if __name__ == "__main__":
    setup_cloudwatch_dashboard()