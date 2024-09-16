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


USER_DATA_SCRIPT = f"""#!/bin/bash
sudo yum update -y
sudo yum install -y httpd
sudo systemctl start httpd
sudo systemctl enable httpd
sudo chmod -R 755 /var/www/html/
sudo AWS_ACCESS_KEY_ID={ACCESS_KEY} AWS_SECRET_ACCESS_KEY={SECRET_KEY} aws s3 cp s3://bucket1234598765/website/index.html /var/www/html/index.html
sudo systemctl restart httpd
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
