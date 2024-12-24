import json
import pandas as pd
import boto3

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    bucket_name = 'finalprojectedubot'
    file_key = 'energy_consumption_data.csv'
    
   
    s3_client.download_file(bucket_name, file_key, '/tmp/energy_consumption_data.csv')
    
    
    df = pd.read_csv('/tmp/energy_consumption_data.csv')
    
    
    df['consumption'] = df['consumption'] * 2
    
   
    df.to_csv('/tmp/transformed_data.csv', index=False)
    
    
    s3_client.upload_file('/tmp/transformed_data.csv', bucket_name, 'transformed_energy_consumption_data.csv')
    
    return {
        'statusCode': 200,
        'body': json.dumps('Data transformation completed successfully')
    }
