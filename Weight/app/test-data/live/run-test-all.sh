#!/bin/bash
#set -x
clear
echo 
export SLEEP=9
#export SLEEP=0
./run-test-health.sh
./run-test-session-prod.sh
./run-test-weight-prod.sh
./run-test-weight-get.sh
./run-test-unknown.sh
./run-test-item-prod.sh
./run-test-batch-weight.sh
