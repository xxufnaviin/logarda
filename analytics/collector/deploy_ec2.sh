# run from root
# take collectors folder into ec2 instance and execute schedule_collectors.sh

scp 

ssh -i "logarda.pem" ubuntu@ec2-54-179-136-16.ap-southeast-1.compute.amazonaws.com 

cd collectors/ && chmod +x schedule_collectors.sh && ./schedule_collectors.sh