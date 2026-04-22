# run both together after building in ec2
# run cron jobs instead now
# current directory /collector

# build docker images
docker build -t collector:latest -f Dockerfile .

# add cron jobs to run both containers and remove them after done
(
echo "*/15 * * * * /usr/bin/docker run --env-file /home/ubuntu/ingestion/.env --rm collector:latest metrics/metrics_collector.py"; 
echo "*/15 * * * * /usr/bin/docker run --env-file /home/ubuntu/ingestion/.env --rm collector:latest logs/logs_collector.py"
) | crontab -
