#!/bin/bash

pkill -f python3

nohup python3 main.py  > bot.log 2>&1 &

