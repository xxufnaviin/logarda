# run from root
# take collectors folder into ec2 instance and execute schedule_collectors.sh

scp -r -i "logarda.pem" analytics/collector ubuntu@ec2-54-179-169-27.ap-southeast-1.compute.amazonaws.com:/home/ubuntu 

ssh -i "logarda.pem" ubuntu@ec2-54-179-169-27.ap-southeast-1.compute.amazonaws.com << 'EOF'
cd collector/ && chmod +x schedule_collectors.sh && ./schedule_collectors.sh 
EOF
