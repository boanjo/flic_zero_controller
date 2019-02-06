#!/bin/sh
sudo ./flicd -d -f data/flic.sqlite3
nohup python3 flic_controller.py &
