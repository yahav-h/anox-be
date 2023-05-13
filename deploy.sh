#!/usr/bin/env bash

cd ./anox-fe
sudo nohup npm start-ui
cd ../
sudo nohup ./startup_script.sh &
