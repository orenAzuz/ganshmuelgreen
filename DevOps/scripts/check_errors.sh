#!/bin/sh
set -e

. $1/env.ini

cd $LOGS

touch errors.log

export CHECK_LOG='test.log'

export count=$(wc -l <errors.log)
( $count > 0 )  && (cat errors.log | grep error > ${CHECK_LOG}) || touch ${CHECK_LOG} 
#echo "count first 1"
#echo "count 2"
(( $(wc -l <$CHECK_LOG) >  0 ))  && cat $CHECK_LOG || echo "OK"
