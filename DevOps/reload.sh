#!/bin/sh
echo "reload in progress ...."
cd $GIT_HOME/DevOps
. ./env.ini
$SCRIPTS/down 0
$SCRIPTS/up $(pwd) 0 
