@ECHO OFF
:: This batch sets autorun on logging on for DMonitor
TITLE DMonitor Autorun
SET /P APP_PATH=Input path to DMonitor.exe:
schtasks /Create /tn "DMonitor" /sc onlogon /tr "%APP_PATH%"
PAUSE