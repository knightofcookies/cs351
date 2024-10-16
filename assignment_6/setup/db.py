import boto3

# Create an RDS client
rds = boto3.client('rds')

response = rds.create_db_instance(
    DBInstanceIdentifier='feedback-db-3',
    MasterUsername='flaskapp',
    MasterUserPassword='flaksapp',
    DBInstanceClass='db.t3.micro',
    Engine='mysql',
    AllocatedStorage=20,
    VpcSecurityGroupIds=['sg-0e7e357d262c268b3'],
    PubliclyAccessible=True
)

print(response)
