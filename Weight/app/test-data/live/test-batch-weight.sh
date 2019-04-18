#!/bin/bash
#set -x
echo 'Call: '$2
curl -X POST -X POST http://$1/batch-weight/$2
sleep $SLEEP
echo 
