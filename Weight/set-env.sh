# EXAMPLE
# read in via: source <filename>
export APP_DATA_PATH=/home/system/devops/w3/ganshmuelgreen/Weight/app/in
export DB_DATA_PATH=/home/system/devops/w3/ganshmuelgreen/Weight/mysql/datadir
export DB_SCRIPT_PATH=/home/system/devops/w3/ganshmuelgreen/Weight/mysql/scripts

# set the environmental variables according to your filesystem, create directories if needed
# run docker-compose up
# it will create two containers called mysql-c and weigh-app-c, you can see them running with docker ps
# to enter the app run docker exec -it weigh-app-c sh
# it will be able to communicate with the db accessing it with the image name mysql-c
