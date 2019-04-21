#!/bin/bash
#set -x

echo
echo "WEIGHT (GET) ENDPOINT:"
echo ======================
echo
echo "Query between 2019-03-27 09:00:00 and 2019-04-17 09:00:00:"
curl "http://18.222.236.224:8081/weight?from=20190327090000&to=20190417090000"
sleep $SLEEP
echo
echo

echo "Same time with filter 'in':"
curl "http://18.222.236.224:8081/weight?from=20190327090000&to=20190417090000&filter=out"
sleep $SLEEP
echo
echo

echo "Same time with filter 'out':"
curl "http://18.222.236.224:8081/weight?from=20190327090000&to=20190417090000&filter=in"
sleep $SLEEP
echo
echo
echo
