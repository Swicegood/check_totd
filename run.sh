#!/bin/bash

# Parameterize the directory path
DIR_PATH="/mnt/user/appdata/check_totd/result"

# if result/result.txt exists, remove it
if [ -f $DIR_PATH/result.txt ]; then
  rm $DIR_PATH/result.txt
fi

# Build the container
docker build -t jagadguru/check_totd .
docker push jagadguru/check_totd

# Run the container
docker run --rm -i -v $DIR_PATH:/app/result jagadguru/check_totd

# if result/result.txt exists, read it and send it to nagios
if [ -f $DIR_PATH/result.txt ]; then
  cat $DIR_PATH/result.txt
  docker run --rm -e EXTERNAL_COMMAND="$(cat $DIR_PATH/result.txt)" jagadguru/send_nsca
else
  echo "result.txt not found"
fi
