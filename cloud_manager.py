import boto3
import os
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