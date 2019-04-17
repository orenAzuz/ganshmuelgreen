#!/bin/bash
#source ./set-env.sh
cd $GIT_HOME/Provider_payment
docker-compose build && docker-compose up
