# run both together after building in ec2
# run cron jobs instead now
# current directory analytics/collector

# build docker images
docker build -t metric_collector:latest metrics/
docker build -t logs_collector:latest logs/

# add cron jobs to run both containers and remove them after done
(
echo "*/15 * * * * docker run --rm metric_collector:latest"; 
echo "*/15 * * * * docker run --rm logs_collector:latest"
) | crontab -
