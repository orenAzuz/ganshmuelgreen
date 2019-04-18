#!/bin/sh
echo "Reload is in progress ...."
cd $GIT_HOME/DevOps
git checkout ${BRANCH}
git pull origin ${BRANCH}

echo "Starting build containers ..."
LOGS=$GIT_HOME/DevOps/logs
rm -f $LOGS/*

rm -rf $GIT_HOME/Weight/mysql/datadir
mkdir -p $GIT_HOME/Weight/mysql/datadir
mkdir -p ${HOME}/billdb


weigh_compose=$GIT_HOME/Weight/docker-compose.yml
bill_compose=$GIT_HOME/Provider_payment/docker-compose.yml

for i in $weigh_compose $bill_compose ; do 
echo "compose file is ${i}"
	echo && echo "Upload process says: docker-compose stop" && \	
	#docker-compose --file "${i}" stop && \
	#echo "Upload process says: docker-compose rm ..." && \
	#docker-compose --file "${i}" rm -f && \
	echo "Upload process says: docker-compose build ..." && \
	#docker-compose build --no-cache --file "${i}"  && \
	echo "Upload process says: docker-compose up ..." && \
        docker-compose --file "${i}" up  1>> $LOGS/out.log 2>>$LOGS/
	#docker-compose --file "${i}" up --force-recreate --remove-orphans 1>> $LOGS/out.log 2>>$LOGS/errors.log 
done



