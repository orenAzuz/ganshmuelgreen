#!/bin/sh
echo "reload in progress ...."
cd $GIT_HOME/DevOps
git checkout master
git pull origin master

echo $PWD
. ./env.ini
$SCRIPTS/down
$SCRIPTS/up $(pwd) 
