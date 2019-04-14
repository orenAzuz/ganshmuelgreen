#!/bin/sh

if [ "$#" -ne 1 ]
then
  PORT=5000
else
  PORT=$1
fi

export PORT=$PORT
python3 chat.py $PORT