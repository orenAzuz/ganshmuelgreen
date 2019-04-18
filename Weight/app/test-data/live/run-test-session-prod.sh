#!/bin/bash
echo
echo SESSION ENDPOINT:
echo =================
echo

echo "Test invalid session:"
./test-session.sh 18.222.236.224:8081 1000
echo "Test valid 'in' session: (request approved to add extra field)"
./test-session.sh 18.222.236.224:8081 10
echo "Test valid 'out' session:"
./test-session.sh 18.222.236.224:8081 13
echo "Test valid 'out' session:"
./test-session.sh 18.222.236.224:8081 15

