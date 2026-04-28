# run from root
# take collectors folder into ec2 instance and execute schedule_collectors.sh

# set username
USERNAME=$1

scp -r -i "logarda.pem" data/ingestion ubuntu@ec2-54-179-169-27.ap-southeast-1.compute.amazonaws.com:/home/ubuntu
scp -r -i "logarda.pem" ./utils ubuntu@ec2-54-179-169-27.ap-southeast-1.compute.amazonaws.com:/home/ubuntu/ingestion 
scp -r -i "logarda.pem" ./config ubuntu@ec2-54-179-169-27.ap-southeast-1.compute.amazonaws.com:/home/ubuntu/ingestion 

ssh -i "logarda.pem" ubuntu@ec2-54-179-169-27.ap-southeast-1.compute.amazonaws.com << EOF
cd ingestion/ && chmod +x schedule_collectors.sh && ./schedule_collectors.sh "$USERNAME" 
EOF
