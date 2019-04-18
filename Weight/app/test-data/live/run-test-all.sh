#!/bin/bash
#set -x
echo 
export SLEEP=5
./run-test-health.sh
./run-test-session-prod.sh
./run-test-weight-prod.sh
./run-test-unknown.sh
./run-test-item-prod.sh
./run-test-weight-get.sh
