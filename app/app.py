from flask import Flask, request, jsonify
import boto3
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# DB connection
db = mysql.connector.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASS"],
    database=os.environ["DB_NAME"]
)
cursor = db.cursor()

# S3
s3 = boto3.client(
    's3',
aws_key = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret = os.getenv('AWS_SECRET_ACCESS_KEY')
)
BUCKET = os.environ['S3_BUCKET']

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    s3.upload_fileobj(file, BUCKET, file.filename)
    return jsonify({'message': f'Uploaded {file.filename} to S3'})

@app.route('/users', methods=['GET'])
def get_users():
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    return jsonify(result)

@app.route('/user', methods=['POST'])
def add_user():
    data = request.json
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (data['name'], data['email']))
    db.commit()
    return jsonify({'message': 'User added'})

if __name__ == "_main_":
    app.run(host="0.0.0.0", port=5000)
