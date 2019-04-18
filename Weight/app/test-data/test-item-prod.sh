#!/bin/bash
#set -x
echo 'Call: '$2'?from='$3'&to='$4
curl http://18.222.236.224:$1/item/$2'?from='$3'&to='$4
echo 