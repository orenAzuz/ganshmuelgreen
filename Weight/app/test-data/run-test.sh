#!/bin/bash

echo For a container without a truck:
./post.sh 8081 none 3122
./post.sh 8081 none 2122
./post.sh 8081 in 12222
./post.sh 8081 out 1000 A10202
./post.sh 8081 in 33222 A10202
./post.sh 8081 none 2122
echo
