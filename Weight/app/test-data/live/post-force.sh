#!/bin/bash
#set -x
echo 'Call: direction='$2'&truck='$4'&force=true&containers=C-35434,K-8263,K-7943&weight='$3'&unit=kg&produce=oranges'
curl -d 'direction='$2'&truck='$4'&force=true&containers=C-35434,K-8263,K-7943&weight='$3'&unit=kg&produce=oranges' -X POST http://$1/weight
sleep $SLEEP
echo 
echo
