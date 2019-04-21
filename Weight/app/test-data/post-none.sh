#!/bin/bash
set -x
curl -d 'direction='$2'&truck=&force=&containers=C-35434,K-8263,K-7943&weight='$3'&unit=kg&produce=oranges' -X POST http://$1/weight

