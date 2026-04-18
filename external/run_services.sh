# "external" folder is root folder to run this script
chmod +x ./install_docker.sh
chmod +x ./services/start_postgres.sh
chmod +x ./services/start_redis.sh

./install_docker.sh
./services/start_postgres.sh
./services/start_redis.sh