import boto3

def lambda_handler(event, context):
    # Initialize the EC2 client to interact with AWS infrastructure
    ec2 = boto3.client('ec2')
    
    # Read the 'action' parameter passed from the Amazon EventBridge payload
    # If no action is specified, default safely to 'stop'
    action = event.get('action', 'stop')
    
    if action == 'start':
        # Filter for instances that are currently STOPPED and have the Development tag
        filters = [
            {'Name': 'tag:Environment', 'Values': ['Development']},
            {'Name': 'instance-state-name', 'Values': ['stopped']}
        ]
        response = ec2.describe_instances(Filters=filters)
        instance_ids = [inst['InstanceId'] for res in response['Reservations'] for inst in res['Instances']]
        
        if instance_ids:
            print(f"Starting development instances: {instance_ids}")
            ec2.start_instances(InstanceIds=instance_ids)
            return {'statusCode': 200, 'body': f"Successfully started: {instance_ids}"}
        else:
            print("No stopped development instances found to start.")
            return {'statusCode': 200, 'body': "No instances required starting."}
            
    elif action == 'stop':
        # Filter for instances that are currently RUNNING and have the Development tag
        filters = [
            {'Name': 'tag:Environment', 'Values': ['Development']},
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
        response = ec2.describe_instances(Filters=filters)
        instance_ids = [inst['InstanceId'] for res in response['Reservations'] for inst in res['Instances']]
        
        if instance_ids:
            print(f"Stopping development instances: {instance_ids}")
            ec2.stop_instances(InstanceIds=instance_ids)
            return {'statusCode': 200, 'body': f"Successfully stopped: {instance_ids}"}
        else:
            print("No running development instances found to stop.")
            return {'statusCode': 200, 'body': "No instances required stopping."}
            
    return {'statusCode': 400, 'body': "Invalid action specified in EventBridge payload."}
