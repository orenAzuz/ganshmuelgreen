#!/bin/bash
BLUE='\033[0;34m'
NC='\033[0m'

echo "WEIGHT (POST) ENDPOINT:"
echo =======================
#echo -e "${BLUE}Weigh truck (in) with 3 containers (truck info missing):${NC}"
echo
echo "Weigh truck (in) with 3 containers (truck info missing):"
./post.sh 18.222.236.224:8081 in 12222

echo "Weigh truck (in) with 3 containers:"
./post.sh 18.222.236.224:8081 in 12222 A10202

echo "Weigh truck (out) with 3 empty containers:"
./post.sh 18.222.236.224:8081 out 1000 A10202

echo "Weigh 'out' after 'out' ... not allowed:"
./post.sh 18.222.236.224:8081 out 1000 A10202

echo "Weigh 'out' after 'out' ... forced:"
./post-force.sh 18.222.236.224:8081 out 1000 A10202

echo "Weigh new truck 'in' after 'out':"
./post.sh 18.222.236.224:8081 in 33222 A10233

echo "Weigh 'in' after 'in' ... not allowed:"
./post.sh 18.222.236.224:8081 in 33222 A10233

echo "Weigh 'in' after 'in' ... forced:"
./post-force.sh 18.222.236.224:8081 in 33222 A10233

echo "Weigh truck (out) with 3 empty containers:"
./post.sh 18.222.236.224:8081 out 1000 A10233

echo "Weigh container without a truck:"
./post.sh 18.222.236.224:8081 none 3122

echo "Using invalid unit ... Weigh new truck 'in' after 'out':"
./post-lbs-kg.sh 18.222.236.224:8081 in 33222 A10233 lb

echo "Using pounds ... Weigh new truck 'in' after 'out' (converts & stores as kg):"
./post-lbs-kg.sh 18.222.236.224:8081 in 33222 A10233 lbs


