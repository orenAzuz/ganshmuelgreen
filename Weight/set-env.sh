# EXAMPLE
# read in via: source <filename>
export APP_DATA_PATH=./app/in
export DB_DATA_PATH=./mysql/datadir
# this script directory is intended for scripts to be manually run - during development
export DB_SCRIPT_PATH=./mysql/scripts
# this script directory is mounted into MySQL container in a location that causes it to auto-run all scripts there
export DB_AUTO_RUN_SCRIPTS=./mysql/auto-run-scripts

# set the environmental variables according to your filesystem, create directories if needed
# run docker-compose up
# it will create two containers called mysql-c and weigh-app-c, you can see them running with docker ps
# to enter the app run docker exec -it weigh-app-c sh
# it will be able to communicate with the db accessing it with the image name mysql-c
