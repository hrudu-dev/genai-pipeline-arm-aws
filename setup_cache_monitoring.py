#!/usr/bin/env python3
"""
Set up CloudWatch dashboard for cache performance monitoring
"""

import boto3
import json
import argparse
import time

# AWS credentials
AWS_ACCESS_KEY_ID = "AKIAQCJFIBGQKP7OBYFN"
AWS_SECRET_ACCESS_KEY = "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"
AWS_DEFAULT_REGION = "us-east-1"

def setup_cache_dashboard(function_name, table_name='GenAIPipelineCache'):
    """Set up CloudWatch dashboard for cache performance monitoring"""
    print(f"Setting up CloudWatch dashboard for cache performance monitoring")
    
    # Create CloudWatch client
    cloudwatch = boto3.client('cloudwatch',
                            region_name=AWS_DEFAULT_REGION,
                            aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    
    # Dashboard name
    dashboard_name = "GenAIPipelineCacheDashboard"
    
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
                        ["AWS/Lambda", "Invocations", "FunctionName", function_name, {"stat": "Sum"}]
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
                        ["AWS/Lambda", "Duration", "FunctionName", function_name, {"stat": "Average"}],
                        ["AWS/Lambda", "Duration", "FunctionName", function_name, {"stat": "Maximum"}]
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
                        ["AWS/DynamoDB", "ConsumedReadCapacityUnits", "TableName", table_name, {"stat": "Sum"}],
                        ["AWS/DynamoDB", "ConsumedWriteCapacityUnits", "TableName", table_name, {"stat": "Sum"}]
                    ],
                    "view": "timeSeries",
                    "stacked": False,
                    "region": AWS_DEFAULT_REGION,
                    "title": "DynamoDB Consumed Capacity",
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
                        ["AWS/DynamoDB", "SuccessfulRequestLatency", "TableName", table_name, "Operation", "GetItem", {"stat": "Average"}],
                        ["AWS/DynamoDB", "SuccessfulRequestLatency", "TableName", table_name, "Operation", "PutItem", {"stat": "Average"}]
                    ],
                    "view": "timeSeries",
                    "stacked": False,
                    "region": AWS_DEFAULT_REGION,
                    "title": "DynamoDB Latency",
                    "period": 300
                }
            },
            {
                "type": "log",
                "x": 0,
                "y": 12,
                "width": 24,
                "height": 6,
                "properties": {
                    "query": f"SOURCE '/aws/lambda/{function_name}' | filter @message like 'Cache hit' or @message like 'Cache miss' | stats count() as count by bin(5m), strcontains(@message, 'Cache hit') as cache_hit | sort @timestamp desc",
                    "region": AWS_DEFAULT_REGION,
                    "title": "Cache Hit/Miss Ratio",
                    "view": "table"
                }
            }
        ]
    }
    
    # Create or update dashboard
    try:
        response = cloudwatch.put_dashboard(
            DashboardName=dashboard_name,
            DashboardBody=json.dumps(dashboard_body)
        )
        
        print(f"Dashboard created: {dashboard_name}")
        print(f"Dashboard URL: https://{AWS_DEFAULT_REGION}.console.aws.amazon.com/cloudwatch/home?region={AWS_DEFAULT_REGION}#dashboards:name={dashboard_name}")
        
        # Create cache hit/miss metric filter
        logs_client = boto3.client('logs',
                                 region_name=AWS_DEFAULT_REGION,
                                 aws_access_key_id=AWS_ACCESS_KEY_ID,
                                 aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        
        try:
            logs_client.put_metric_filter(
                logGroupName=f"/aws/lambda/{function_name}",
                filterName="CacheHitMissFilter",
                filterPattern="[timestamp, request_id, level, message, cache_status]",
                metricTransformations=[
                    {
                        'metricName': 'CacheHit',
                        'metricNamespace': 'GenAIPipeline',
                        'metricValue': '1',
                        'defaultValue': 0,
                        'dimensions': {
                            'FunctionName': function_name
                        }
                    }
                ]
            )
            
            print("Created metric filter for cache hits/misses")
        except Exception as e:
            print(f"Error creating metric filter: {str(e)}")
        
        return dashboard_name
    except Exception as e:
        print(f"Error creating dashboard: {str(e)}")
        return None

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Set up CloudWatch dashboard for cache performance monitoring')
    parser.add_argument('--function', '-f', default='GenAIPipelineTest2', help='Lambda function name')
    parser.add_argument('--table', '-t', default='GenAIPipelineCache', help='DynamoDB table name')
    
    args = parser.parse_args()
    
    setup_cache_dashboard(args.function, args.table)

if __name__ == "__main__":
    main()