#!/bin/sh
echo "Input path to DMonitorLinux"
read APP_PATH

sed "s|path|$APP_PATH|" dmonitor.service.template > dmonitor.service
sudo cp dmonitor.service /lib/systemd/system

sudo systemctl daemon-reload
sudo systemctl enable dmonitor.service
sudo systemctl start dmonitor.service