#!/bin/bash
#set -x

echo Weight 'GET':
echo =============
echo
echo "Looking BETWEEN 2019-03-27 09:00:00 to 2019-04-17 09:00:00"
curl http://18.222.236.224:8081/weight?from=20190327090000&to=20190417090000
echo

echo "Same time with filter 'in'"
curl http://18.222.236.224:8081/weight?from=20190327090000&to=20190417090000&filter=out
echo

echo "Same time with filter 'out'"
curl http://18.222.236.224:8081/weight?from=20190327090000&to=20190417090000&filter=in
echo
