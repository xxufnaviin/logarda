# run from root
# take env and place it in ec2

scp -r -i "logarda.pem" config/.env $EC2_USER@$EC2_HOST:/home/$EC2_USER/config

# pull the latest docker image into the repo
# add cron jobs to run containers and remove them after done
ssh -i "logarda.pem" $EC2_USER@$EC2_HOST << 'EOF'
docker pull repo:latest
(echo "*/15 * * * * /usr/bin/docker run --env-file /home/ubuntu/ingestion/config/.env --rm collector:latest main.py") | crontab -
EOF
