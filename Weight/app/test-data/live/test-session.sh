#!/bin/bash
#set -x
echo 'Call: /session/'$2
curl http://$1/session/$2
sleep $SLEEP
echo 
echo 
