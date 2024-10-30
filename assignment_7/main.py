import boto3
from datetime import datetime
import time

# Configure AWS credentials
aws_access_key = "AKIATTSKFSJPTJUTJNPJ"
aws_secret_key = ""
aws_region = "ap-south-1"

# Initialize the Elastic Beanstalk client

eb_client = boto3.client(
    "elasticbeanstalk",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region,
)

cf_client = boto3.client(
    "cloudfront",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region,
)


def create_new_application():
    app_name = "portfolio-app"
    app_description = "portfolio application"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        eb_client.create_application(
            ApplicationName=app_name, Description=app_description
        )

        print("Application created successfully.")
        print(f"Application Name: {app_name}")
        print(f"Application Description: {app_description}")
        print(f"Current Time and Date: {current_time}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def show_all_apps():
    try:
        response = eb_client.describe_applications()
        applications = response.get("Applications", [])

        if applications:
            print("List of Applications:")
            for app in applications:
                app_name = app["ApplicationName"]
                app_description = app.get("Description", "No description available")
                print(f"Application Name: {app_name}")
                print(f"Application Description: {app_description}")
                print("---")
        else:
            print("No applications found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def create_new_environment():
    env_name = "portfolio-app-env1"
    solution_stack_name = "64bit Amazon Linux 2023 v6.2.2 running Node.js 20"
    version_label = "v1.0"
    iam_instance_profile_name = "arn:aws:iam::248189915743:instance-profile/AWSElasticBeanstalkWebTierRole"  # Replace with your IAM instance profile ARN

    try:
        eb_client.create_environment(
            ApplicationName="portfolio-app",
            EnvironmentName=env_name,
            SolutionStackName=solution_stack_name,
            VersionLabel=version_label,
            OptionSettings=[
                {
                    "Namespace": "aws:autoscaling:launchconfiguration",
                    "OptionName": "SecurityGroups",
                    "Value": "sg-0e7e357d262c268b3",
                },
                {
                    "Namespace": "aws:autoscaling:asg",
                    "OptionName": "MinSize",
                    "Value": "1",  # Minimum number of instances
                },
                {
                    "Namespace": "aws:autoscaling:asg",
                    "OptionName": "MaxSize",
                    "Value": "1",  # Maximum number of instances
                },
                {
                    "Namespace": "aws:autoscaling:asg",
                    "OptionName": "Cooldown",
                    "Value": "60",  # Scaling cooldown period in seconds
                },
                {
                    "Namespace": "aws:autoscaling:launchconfiguration",
                    "OptionName": "IamInstanceProfile",
                    "Value": iam_instance_profile_name,
                },
                {
                    "Namespace": "aws:ec2:vpc",
                    "OptionName": "VPCId",
                    "Value": "vpc-027fe622687640277",  # Your VPC ID
                },
                {
                    "Namespace": "aws:ec2:vpc",
                    "OptionName": "Subnets",
                    "Value": "subnet-0918b855dcac5dc0f",
                },
                {
                    "Namespace": "aws:ec2:vpc",
                    "OptionName": "ELBSubnets",
                    "Value": "subnet-0918b855dcac5dc0f, subnet-0d249c33eb1162f74, subnet-0f890cffb6a13f728",
                },
                {
                    "Namespace": "aws:elb:loadbalancer",
                    "OptionName": "SecurityGroups",
                    "Value": "sg-0e7e357d262c268b3",
                },
            ],
        )

        print("Environment creation initiated.")
        print(f"Environment Name: {env_name}")
        print(f"Solution Stack Name: {solution_stack_name}")
        print(f"Version Label: {version_label}")

        # Wait for the environment to become "Ready" or "Terminated"
        while True:
            environment_info = eb_client.describe_environments(
                ApplicationName="portfolio-app",
                EnvironmentNames=[env_name],
            )
            environment_status = environment_info["Environments"][0]["Status"]
            if environment_status in ("Ready", "Terminated"):
                break
            time.sleep(10)  # Wait for 10 seconds before checking again

        if environment_status == "Ready":
            environment_url = environment_info["Environments"][0]["CNAME"]
            print("Environment created successfully.")
            print(f"Status: {environment_status}")
            print(f'Health: {environment_info["Environments"][0]["Health"]}')
            print(f'Endpoint URL: {environment_info["Environments"][0]["EndpointURL"]}')
            print(f"Domain Name (CNAME): {environment_url}")
        elif environment_status == "Terminated":
            print("Environment creation failed.")
            print(f"Status: {environment_status}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def create_application_version():
    response = eb_client.create_application_version(
        ApplicationName="portfolio-app",
        AutoCreateApplication=True,
        Description="portfolio-app-v1",
        Process=True,
        SourceBundle={
            "S3Bucket": "assignment-7",
            "S3Key": "app.zip",
        },
        VersionLabel="v1.0",
    )
    print(response)


def update_or_say_deploy_to_environment():
    response = eb_client.update_environment(
        ApplicationName="portfolio-app",
        EnvironmentName="portfolio-app-env1",
        VersionLabel="v1.0",
    )

    print(response)


def create_distribution():
    """Create a Cloudfront Distribution."""
    try:
        # Elastic Beanstalk Environment
        elasticbeanstalk_domain = "awseb-e-j-AWSEBLoa-I1U1QRL16III-528946907.ap-south-1.elb.amazonaws.com"  # Replace with your Beanstalk environment URL

        # S3 Bucket for Static Content
        s3_bucket_name = "assignment-7"  # Replace with your S3 bucket name

        # Create a CloudFront distribution configuration
        distribution_config = {
            "CallerReference": str(int(time.time())),  # Unique timestamp
            "DefaultCacheBehavior": {
                "TargetOriginId": "beanstalk-origin",
                "ViewerProtocolPolicy": "redirect-to-https",
                "CachePolicyId": "658327ea-f89d-4fab-a63d-7e88639e58f6",  # Default CloudFront cache policy ID
                "OriginRequestPolicyId": "216adef6-5c7f-47e4-b989-5492eafa07d3",  # Default CloudFront origin request policy ID
            },
            "Comment": "CDN for portfolio-app",
            "Enabled": True,
            "Origins": {
                "Quantity": 2,  # Two origins: Elastic Beanstalk and S3
                "Items": [
                    {
                        "Id": "beanstalk-origin",
                        "DomainName": elasticbeanstalk_domain,
                        "CustomOriginConfig": {
                            "HTTPPort": 80,
                            "HTTPSPort": 443,
                            "OriginProtocolPolicy": "http-only",
                        },
                    },
                    {
                        "Id": "s3-origin",
                        "DomainName": s3_bucket_name + ".s3.amazonaws.com",
                        "S3OriginConfig": {
                            "OriginAccessIdentity": "",
                        },
                    },
                ],
            },
            "PriceClass": "PriceClass_All",
        }

        distribution = cf_client.create_distribution(
            DistributionConfig=distribution_config
        )
        print(
            f"CloudFront distribution created with ID: {distribution['Distribution']['Id']}"
        )
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Create New Application in Beanstalk")
        print("2. Show_all_apps in beanstalk")
        print("3. Create Environment for a Newly Application")
        print("4. create_cloudfront_distribution")
        print("5. Create New Version of Existing Application")
        print("6. update_or_say_deploy_to_environment")

        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_new_application()
        elif choice == "2":
            show_all_apps()
        elif choice == "3":
            create_new_environment()
        elif choice == "4":
            create_distribution()
        elif choice == "5":
            create_application_version()
        elif choice == "6":
            update_or_say_deploy_to_environment()
        elif choice == "7":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main_menu()
