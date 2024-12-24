import json
import pandas as pd
import numpy as np
import boto3

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    bucket_name = 'finalprojectedubot'
    file_key = 'energy_consumption_data.csv'
    
    
    s3_client.download_file(bucket_name, file_key, '/tmp/energy_consumption_data.csv')
    
  
    df = pd.read_csv('/tmp/energy_consumption_data.csv')
    
    mean = df['consumption'].mean()
    std_dev = df['consumption'].std()
    threshold = mean + 2 * std_dev
    
    
    anomalies = df[df['consumption'] > threshold]
    
   
    anomalies.to_csv('/tmp/anomalies.csv', index=False)
    
   
    s3_client.upload_file('/tmp/anomalies.csv', bucket_name, 'anomalies_energy_consumption_data.csv')
    
    return {
        'statusCode': 200,
        'body': json.dumps('Anomaly detection completed successfully')
    }
