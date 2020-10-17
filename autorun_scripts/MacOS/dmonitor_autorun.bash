 #!/bin/bash
 
echo "Input path to DMonitorMacOS.zip"
read APP_PATH
sed "s|path|$APP_PATH|" dmonitor.plist.template > dmonitor.plist

cp dmonitor.plist ~/Library/LaunchAgents

launchctl load ~/Library/LaunchAgents/dmonitor.plist