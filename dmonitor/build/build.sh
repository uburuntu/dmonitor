#!/bin/bash

pyinstaller --noconsole --noconfirm --clean --onefile --name DMonitor --paths .. --icon icon.ico ../main.py
