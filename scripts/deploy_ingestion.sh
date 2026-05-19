# run from root
# take env and place it in ec2

ssh -i logarda.pem $EC2_USER@$EC2_HOST "mkdir -p /home/$EC2_USER/config"
scp -i logarda.pem config/.env $EC2_USER@$EC2_HOST:/home/$EC2_USER/config/.env

# pull the latest docker image into the repo
# add cron jobs to run containers and remove them after done
ssh -i "logarda.pem" $EC2_USER@$EC2_HOST << EOF
docker pull $ECR_IMAGE
(echo "*/15 * * * * /usr/bin/docker run --env-file /home/ubuntu/ingestion/config/.env --rm $ECR_IMAGE main.py") | crontab -
EOF
