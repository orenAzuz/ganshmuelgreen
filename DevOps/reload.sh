#!/bin/sh
echo "reload in progress ...."
cd $GIT_HOME/DevOps
git checkout master
git pull origin master

. ./env.ini
$SCRIPTS/down 0
$SCRIPTS/up $(pwd) 0 
