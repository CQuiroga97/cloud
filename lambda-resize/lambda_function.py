import boto3
from PIL import Image
import io

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    response = s3.get_object(Bucket=bucket, Key=key)
    image_data = response['Body'].read()
    image = Image.open(io.BytesIO(image_data))

    # Redimensionar imagen
    resized_image = image.resize((300, 300))
    buffer = io.BytesIO()
    resized_image.save(buffer, format=image.format)
    buffer.seek(0)

    # Guardar imagen redimensionada en carpeta "resized/"
    new_key = f"resized/{key}"
    s3.put_object(Bucket=bucket, Key=new_key, Body=buffer)

    return {
        'statusCode': 200,
        'body': f'Redimensionado y guardado en {new_key}'
    }