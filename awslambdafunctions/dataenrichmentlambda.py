import json
import pandas as pd
import boto3
from datetime import datetime

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    bucket_name = 'finalprojectedubot'
    file_key = 'energy_consumption_data.csv'
    
  
    s3_client.download_file(bucket_name, file_key, '/tmp/energy_consumption_data.csv')
    
    
    df = pd.read_csv('/tmp/energy_consumption_data.csv')
    
    
    df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    
    df.to_csv('/tmp/enriched_data.csv', index=False)
    
    s3_client.upload_file('/tmp/enriched_data.csv', bucket_name, 'enriched_energy_consumption_data.csv')
    
    return {
        'statusCode': 200,
        'body': json.dumps('Data enrichment completed successfully')
    }
