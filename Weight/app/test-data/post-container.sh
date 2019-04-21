#!/bin/bash
#set -x
echo 'Call: direction='$2'&truck='$4'&force=&containers='$5'&weight='$3'&unit=kg&produce=oranges'
curl -d 'direction='$2'&truck='$4'&force=&containers='$5'&weight='$3'&unit=kg&produce=oranges' -X POST http://$1/weight
echo 
echo
