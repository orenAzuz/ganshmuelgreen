# This will create two containers called mysql-c and weigh-app-c, you can see them running with docker ps
# to enter the app run docker exec -it weigh-app-c sh
# it will be able to communicate with the db accessing it with the image name mysql-c

#export APP_DATA_PATH=./app/in

# NB: this needs to be "mysql-c" to run in the container (IT IS SET ACCORDINGLY IN docker-compose-yml).  For local DEV, this is localhost 
#export DB_HOST=localhost
# This path is for DB data to persist regardless of container
#export DB_DATA_PATH=$GIT_HOME/Weight/mysql/datadir
# This script directory is intended for scripts to be manually run - during development
#export DB_SCRIPT_PATH=$GIT_HOME/Weight/mysql/scripts
# This script directory is mounted into MySQL container in a location that causes it to auto-run all scripts there
#export DB_AUTO_RUN_SCRIPTS=./mysql/auto-run-scripts
export GIT_HOME=$PWD

mkdir -p ./mysql/datadir

docker-compose down
docker-compose up
