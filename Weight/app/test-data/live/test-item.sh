#!/bin/bash
#set -x
echo 'Call: '$2'?from='$3'&to='$4
curl http://localhost:$1/item/$2'?from='$3'&to='$4
sleep $SLEEP
echo 
