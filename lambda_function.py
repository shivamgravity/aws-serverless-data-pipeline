import json
import boto3
import random
import datetime

s3 = boto3.client('s3')
BUCKET_NAME = 'your-s3-bucket-name'

def lambda_handler(event, context):
    # 1. Generate Demo Data
    products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor']
    data = {
        'order_id': random.randint(1000, 9999),
        'product': random.choice(products),
        'price': random.randint(20, 500),
        'date': datetime.datetime.now().isoformat()
    }
    
    # 2. Define File Name (it is unique based on time)
    file_name = f"sales_data_{data['order_id']}.json"
    
    # 3. Save to S3 bucket
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=file_name,
        Body=json.dumps(data)
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(f"Saved {file_name} to S3")
    }