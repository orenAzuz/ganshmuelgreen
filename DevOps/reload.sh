#!/bin/sh
echo "Reload is in progress ...."
cd $GIT_HOME/DevOps
git checkout ${BRANCH}
git pull origin ${BRANCH}

echo "Starting build containers ..."
#export LOGS=$GIT_HOME/DevOps/logs

#rm -f $LOGS/*
sudo rm -rf $HOME/billdb
mkdir $HOME/billdb
chmod 777 $HOME/billdb
sudo rm -rf $GIT_HOME/Weight/mysql/datadir
mkdir -p $GIT_HOME/Weight/mysql/datadir
chmod 777 $GIT_HOME/Weight/mysql/datadir

weigh_compose=$GIT_HOME/Weight/docker-compose.yml
bill_compose=$GIT_HOME/Provider_payment/docker-compose.yml

for i in $bill_compose $weigh_compose  ; do 
	echo "compose file is ${i}"
	echo && echo "Upload process says: docker-compose down" && \	
	docker-compose --file "${i}"  down && \	
	echo "Upload process says: docker-compose build ..." && \
	docker-compose   --file "${i}" build --no-cache  && \
	echo "Upload process says: docker-compose up ..." && \
	docker-compose --file "${i}" up --force-recreate --remove-orphans &
#1> $LOGS/out.log 2>$LOGS/errors.log 
done



