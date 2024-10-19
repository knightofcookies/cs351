import os
from dotenv import load_dotenv
import boto3

load_dotenv()

ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
REGION_NAME = os.getenv("REGION_NAME")

session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=REGION_NAME,
)

ec2 = session.resource("ec2")


USER_DATA_SCRIPT = """#!/bin/bash
sudo yum update -y
sudo yum install python3
sudo wget https://github.com/knightofcookies/cs351/raw/refs/heads/main/assignment_6/app.py
mkdir templates
cd templates
sudo wget https://github.com/knightofcookies/cs351/raw/refs/heads/main/assignment_6/templates/index.html
cd ..
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
pip3 install flask
pip3 install pymysql
python3 app.py
"""

instances = ec2.create_instances(
    ImageId="ami-0e53db6fd757e38c7",  # Replace with your preferred AMI ID
    MinCount=1,
    MaxCount=1,
    InstanceType="t2.micro",
    KeyName="bazinga",  # Replace with your key pair name
    SecurityGroupIds=["sg-0e7e357d262c268b3"],  # Replace with your security group ID
    UserData=USER_DATA_SCRIPT,
)

instance = instances[0]

instance.wait_until_running()

instance.reload()

print(f"Instance is running at {instance.public_dns_name}")

# Port 80 - HTTP
# SSH - Secure Shell
# S3 - 100 buckets/account, unlimited objects, 5TB max per object, 5 GB in one PUT
