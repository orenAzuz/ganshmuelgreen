#!/bin/bash
#set -x
echo 'Call: '$2'?from='$3'&to='$4
curl http://18.222.236.224:8081/$1$2'?from='$3'&to='$4
sleep $SLEEP
echo 
