#!/bin/sh
echo "reload in progress ...."
cd $GIT_HOME
. ./env.ini
$SCRIPTS/down
$SCRIPTS/up $(pwd) 
