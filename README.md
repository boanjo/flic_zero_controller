# flic_zero_controller
A simple python client to do REST action calls to your homeautomation when pressing the flic buttons based on the project fliclib-linux-hci

This is deployed on a PI zero which seems to cover most of my house (i only have 4 flic buttons currently) 3 for lightning and one for garage door opening 

Add something like this to run at reboot (to your /etc/rc.local):
```bash
(
   cd /home/pi/repos/flic_zero_controller
   ./start.sh
)
```
You should include the brackets to run the cd and command in a sub shell.
