from flask import Flask, request, jsonify
import boto3
import psycopg2
import os
from datetime import datetime
app = Flask(__name__)
# Configuración S3
s3 = boto3.client('s3')
BUCKET_NAME = 'imagenes-taller-cristhian'
# Configuración RDS
conn = psycopg2.connect(
    host='imagenesdb2.czyqgkyssdoq.us-east-1.rds.amazonaws.com ',
    database='imagenes',
    user='admin',
    password='!Cristian2396980'
)
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename
    s3.upload_fileobj(file, BUCKET_NAME, filename)

    # Guardar metadatos
    url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}"
    cursor = conn.cursor()
    cursor.execute("INSERT INTO imagenes (nombre, url, fecha_subida) VALUES (%s, %s, %s)",
    (filename, url, datetime.utcnow()))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Imagen subida exitosamente', 'url': url})
if __name__ == '__main__':
    app.run(debug=True)
