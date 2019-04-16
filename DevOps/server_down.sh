#!/bin/sh
echo "reload in progress ...."
cd $GIT_HOME/DevOps
. ./env.ini
$SCRIPTS/down 1
