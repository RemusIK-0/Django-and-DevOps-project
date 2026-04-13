import boto3
import os
import datetime
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def get_s3_buckets():
    try:
        # Creates a boto3 client
        s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        
        # Cerem lista de bucket-uri
        response = s3.list_buckets()
        
        # Extragem doar numele bucket-urilor
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        return buckets

    except (NoCredentialsError, PartialCredentialsError):
        return ["Eroare: Cheile AWS nu sunt configurate corect."]
    except Exception as e:
        return [f"A aparut o eroare: {str(e)}"]
    
def get_ec2_instances():
    try:
        ec2 = boto3.client(
            'ec2',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        
        response = ec2.describe_instances()
        instances = []
        
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instances.append({
                    'id': instance['InstanceId'],
                    'type': instance['InstanceType'],
                    'state': instance['State']['Name'],
                    # Căutăm tag-ul 'Name' dacă există
                    'name': next((tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'), "Fără nume")
                })
        return instances
    except Exception as e:
        return [f"Eroare EC2: {str(e)}"]
    
def get_aws_costs():
    try:
        ce = boto3.client(
            'ce',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name='us-east-1' 
        )

        today = datetime.date.today()
        start_of_month = today.replace(day=1).isoformat()
        end_of_today = today.isoformat()
        
        if start_of_month == end_of_today:
            start_of_month = (today - datetime.timedelta(days=1)).replace(day=1).isoformat()

        response = ce.get_cost_and_usage(
            TimePeriod={'Start': start_of_month, 'End': end_of_today},
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
        )

        amount = float(response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount'])
        return amount
    except Exception as e:
        print(f"Eroare Cost Explorer: {e}")
        return 0.0
    
def get_detailed_costs():
    client = boto3.client('ce', region_name='us-east-1')

    now = datetime.datetime.now()
    start_date = now.strftime('%Y-%m-01')
    end_date = now.strftime('%Y-%m-%d')

    response = client.get_cost_and_usage(
    TimePeriod={'Start': start_date, 'End': end_date},
    Granularity='MONTHLY',
    Metrics=['UnblendedCost'],
    GroupBy=[
        {
            'Type': 'DIMENSION',
            'Key': 'SERVICE'
        }
    ])

    detailed_logs = []
    for group in response['ResultsByTime'][0]['Groups']:
        service_name = group['Keys'][0]
        amount = float(group['Metrics']['UnblendedCost']['Amount'])
        if amount > 0:
            detailed_logs.append({
                'service': service_name,
                'amount': amount,
                'date': end_date
            })
    return detailed_logs
        