#!/bin/bash
#set -x
echo 
./run-test-session-prod.sh
./run-test-weight-prod.sh
./run-test-unknown.sh
