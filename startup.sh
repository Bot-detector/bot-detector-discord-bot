#!/bin/bash

if [ -e pid.txt ]
then
    kill -9 `cat pid.txt`
    rm pid.txt
else
    echo "no file bro"

nohup python3 main.py  > bot.log 2>&1 &
echo $! > pid.txt

fi
