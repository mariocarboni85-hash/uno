#!/bin/bash
# Deploy Super Agent su AWS EC2 + S3
# Prerequisiti: AWS CLI configurato

# Parametri
APP_NAME="super-agent"
EC2_TYPE="t3.medium"
REGION="eu-west-1"
S3_BUCKET="super-agent-storage"

# Crea bucket S3
aws s3 mb s3://$S3_BUCKET --region $REGION

# Avvia istanza EC2
INSTANCE_ID=$(aws ec2 run-instances --image-id ami-0c55b159cbfafe1f0 --count 1 --instance-type $EC2_TYPE --key-name my-key --security-group-ids sg-xxxxxxx --subnet-id subnet-xxxxxxx --region $REGION --query 'Instances[0].InstanceId' --output text)

echo "EC2 avviata: $INSTANCE_ID"

# Carica file su S3
aws s3 cp ../dashboard/backend s3://$S3_BUCKET/backend/ --recursive
aws s3 cp ../dashboard/frontend s3://$S3_BUCKET/frontend/ --recursive

echo "Deploy completato su AWS EC2 + S3"