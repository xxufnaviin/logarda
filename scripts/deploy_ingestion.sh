# run from root
# take collectors folder into ec2 instance and execute schedule_collectors.sh

scp -r -i "logarda.pem" data/ingestion $EC2_USER@$EC2_HOST:/home/$EC2_USER
scp -r -i "logarda.pem" ./utils $EC2_USER@$EC2_HOST:/home/$EC2_USER/ingestion 
scp -r -i "logarda.pem" ./config $EC2_USER@$EC2_HOST:/home/$EC2_USER/ingestion 

ssh -i "logarda.pem" $EC2_USER@$EC2_HOST << 'EOF'
cd ingestion/ && chmod +x schedule_collectors.sh && ./schedule_collectors.sh 
EOF
