#!/bin/sh
echo "reload in progress ...."
cd $GIT_HOME/DevOps
git checkout ${BRANCH}
git pull origin ${BRANCH}

. ./env.ini
$SCRIPTS/down 0
$SCRIPTS/up $(pwd) 0 
