# run both together after building in ec2
# run cron jobs instead now
# current directory /collector

# build docker images
# docker build -t collector:latest -f Dockerfile .
docker build -t collector:latest -f data/ingestion/Dockerfile .

# add cron jobs to run containers and remove them after done
(
echo "*/15 * * * * /usr/bin/docker run --env-file /home/ubuntu/ingestion/config/.env --rm collector:latest main.py"
) | crontab -
