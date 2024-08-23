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
apt-get update -y
apt-get install -y apache2
systemctl start apache2
systemctl enable apache2
sudo chmod -R 755 /var/www/html/
sudo curl "https://bucket1234598765.s3.ap-south-1.amazonaws.com/website/index.html" -o /var/www/html/index.html
"""

instances = ec2.create_instances(
    ImageId="ami-0522ab6e1ddcc7055",  # Replace with your preferred AMI ID
    MinCount=1,
    MaxCount=1,
    InstanceType="t2.micro",
    KeyName="bazinga",  # Replace with your key pair name
    SecurityGroupIds=["sg-07c4f01ac3b5e84a3"],  # Replace with your security group ID
    UserData=USER_DATA_SCRIPT,
)

instance = instances[0]

instance.wait_until_running()

instance.reload()

print(f"Instance is running at {instance.public_dns_name}")
