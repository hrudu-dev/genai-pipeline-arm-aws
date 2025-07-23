#!/usr/bin/env python3
"""
Simple cleanup script to stop and delete AWS resources created by the GenAI Pipeline project.
"""

import boto3
import sys

def cleanup_lambda():
    """Delete Lambda functions"""
    print("Cleaning up Lambda functions...")
    lambda_client = boto3.client('lambda')
    
    functions = ["GenAIPipeline-Inference", "GenAIPipelineTest2", "GenAIPipelineMultiRegion"]
    for function in functions:
        try:
            lambda_client.delete_function(FunctionName=function)
            print(f"Deleted Lambda function: {function}")
        except Exception as e:
            print(f"Error deleting Lambda function {function}: {e}")

def cleanup_ec2():
    """Terminate EC2 instances"""
    print("Cleaning up EC2 instances...")
    ec2 = boto3.client('ec2')
    
    try:
        # Find instances with GenAIPipeline tag
        response = ec2.describe_instances(
            Filters=[{'Name': 'tag:Project', 'Values': ['GenAIPipeline']}]
        )
        
        instance_ids = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                if instance['State']['Name'] not in ['terminated', 'shutting-down']:
                    instance_ids.append(instance['InstanceId'])
        
        if instance_ids:
            ec2.terminate_instances(InstanceIds=instance_ids)
            print(f"Terminated EC2 instances: {instance_ids}")
        else:
            print("No EC2 instances found to terminate")
    except Exception as e:
        print(f"Error terminating EC2 instances: {e}")

def cleanup_iam():
    """Delete IAM resources"""
    print("Cleaning up IAM resources...")
    iam = boto3.client('iam')
    
    # Delete test user
    try:
        user_name = 'genai-pipeline-tester'
        
        # Delete access keys
        try:
            keys = iam.list_access_keys(UserName=user_name)['AccessKeyMetadata']
            for key in keys:
                iam.delete_access_key(UserName=user_name, AccessKeyId=key['AccessKeyId'])
        except Exception:
            pass
        
        # Detach policies
        try:
            policies = iam.list_attached_user_policies(UserName=user_name)['AttachedPolicies']
            for policy in policies:
                iam.detach_user_policy(UserName=user_name, PolicyArn=policy['PolicyArn'])
        except Exception:
            pass
        
        # Delete user
        iam.delete_user(UserName=user_name)
        print(f"Deleted IAM user: {user_name}")
    except Exception as e:
        print(f"Error deleting IAM user: {e}")
    
    # Delete role
    try:
        role_name = 'lambda-bedrock-role'
        
        # Detach policies
        try:
            policies = iam.list_attached_role_policies(RoleName=role_name)['AttachedPolicies']
            for policy in policies:
                iam.detach_role_policy(RoleName=role_name, PolicyArn=policy['PolicyArn'])
        except Exception:
            pass
        
        # Delete inline policies
        try:
            policy_names = iam.list_role_policies(RoleName=role_name)['PolicyNames']
            for policy_name in policy_names:
                iam.delete_role_policy(RoleName=role_name, PolicyName=policy_name)
        except Exception:
            pass
        
        # Delete role
        iam.delete_role(RoleName=role_name)
        print(f"Deleted IAM role: {role_name}")
    except Exception as e:
        print(f"Error deleting IAM role: {e}")
    
    # Delete policy
    try:
        policy_name = 'GenAIPipelineTestPolicy'
        
        # Find policy ARN
        policies = iam.list_policies(Scope='Local')['Policies']
        policy_arn = None
        for policy in policies:
            if policy['PolicyName'] == policy_name:
                policy_arn = policy['Arn']
                break
        
        if policy_arn:
            iam.delete_policy(PolicyArn=policy_arn)
            print(f"Deleted IAM policy: {policy_name}")
    except Exception as e:
        print(f"Error deleting IAM policy: {e}")

def cleanup_dynamodb():
    """Delete DynamoDB tables"""
    print("Cleaning up DynamoDB tables...")
    dynamodb = boto3.client('dynamodb')
    
    try:
        tables = dynamodb.list_tables()['TableNames']
        for table in tables:
            if 'genai' in table.lower() or 'pipeline' in table.lower():
                dynamodb.delete_table(TableName=table)
                print(f"Deleted DynamoDB table: {table}")
    except Exception as e:
        print(f"Error deleting DynamoDB tables: {e}")

def cleanup_cloudformation():
    """Delete CloudFormation stacks"""
    print("Cleaning up CloudFormation stacks...")
    cf = boto3.client('cloudformation')
    
    try:
        stacks = cf.list_stacks(
            StackStatusFilter=['CREATE_COMPLETE', 'UPDATE_COMPLETE', 'ROLLBACK_COMPLETE']
        )['StackSummaries']
        
        for stack in stacks:
            if 'genai' in stack['StackName'].lower() or 'pipeline' in stack['StackName'].lower():
                cf.delete_stack(StackName=stack['StackName'])
                print(f"Deleting CloudFormation stack: {stack['StackName']}")
    except Exception as e:
        print(f"Error deleting CloudFormation stacks: {e}")

def main():
    print("GenAI Pipeline AWS Resource Cleanup")
    print("===================================")
    
    confirm = input("This will delete ALL AWS resources created by the GenAI Pipeline project. Continue? (y/n): ")
    if confirm.lower() != 'y':
        print("Cleanup cancelled.")
        return
    
    cleanup_lambda()
    cleanup_ec2()
    cleanup_iam()
    cleanup_dynamodb()
    cleanup_cloudformation()
    
    print("\nCleanup complete! All GenAI Pipeline resources have been deleted or scheduled for deletion.")

if __name__ == "__main__":
    main()