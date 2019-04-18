#!/bin/bash
#set -x
echo 
export SLEEP=2
./run-test-session-prod.sh
./run-test-weight-prod.sh
./run-test-unknown.sh
