#!/bin/bash
#set -x
echo HEALTH ENDPOINT:
echo ================
echo
echo 'Call: /health'
curl http://18.222.236.224:8081/health
echo 
