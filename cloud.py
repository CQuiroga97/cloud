from flask import Flask, request, jsonify
import boto3
import pymysql
from datetime import datetime
import pymysql
app = Flask(__name__)

# Configuración S3
s3 = boto3.client('s3')
BUCKET_NAME = 'imagenes-taller-cristhian'

# Configuración RDS (MySQL)
conn = pymysql.connect(
    host='imagenesdb2.czyqgkyssdoq.us-east-1.rds.amazonaws.com',
    user='admin',
    password='!Cristian2396980',
    database='imagenes',
    port=3306
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
    host = '0.0.0.0'
    port = 5000
    print(f"🚀 Servidor Flask ejecutándose en http://{host}:{port}")
    app.run(host=host, port=port, debug=True)
