#!/bin/bash

echo BATCH-WEIGHT ENDPOINT:
echo ======================
echo

echo Read from containers1.csv \(in kg\), write to database and show output - if data are not already in:
./test-batch-weight.sh 8081 containers1.csv
echo

echo Read from containers2.csv \(in lbs\), write to database and show output - if data are not already in:
./test-batch-weight.sh 8081 containers2.csv
echo

echo Read from containers3.json \(in lbs\), write to database and show output - if data are not already in:
./test-batch-weight.sh 8081 containers3.json
echo

echo Read from ghost-file.txt, the file doesn\'t exist:
./test-batch-weight.sh 8081 ghost-file.txt
echo
