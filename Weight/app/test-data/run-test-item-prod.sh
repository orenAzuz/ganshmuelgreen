#!/bin/bash

echo Search for truck A10005:
./test-item-prod.sh 8081 A10005
echo

echo Search for truck A10005 from the 16th of April 2019 - no entry:
./test-item-prod.sh 8081 A10005 20190416130442
echo


echo Search for container 2030:
./test-item-prod.sh 8081 2030
echo


echo Search for container 2030 from the 1st of January 2019 to 28th of February 2019 - no entry:
./test-item-prod.sh 8081 2030 20190101130442 20190228130442
echo
