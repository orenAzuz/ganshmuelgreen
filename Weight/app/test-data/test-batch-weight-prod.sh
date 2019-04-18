#!/bin/bash
#set -x
echo 'Call: '$2
curl -X POST -X POST http://18.222.236.224:$1/batch-weight/$2
echo 