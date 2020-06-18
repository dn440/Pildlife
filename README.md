# pildlife
Raspberry Pi wildlife camera

# Hardware
PIR sensor
- "- pin" is connected to ground
- "+ pin" is connected to 3.3V power
- middle pin "0" is connected to Raspberry Pi pin 11

# Configuration
To automate the script to run at startup, use:
`crontab -e`

To the bottom add the line:
`@reboot python /home/pi/pildlife/run.py &`
Especially important is the & at the end of the call, since our script runs an infinite loop. Without the `&`, the boot would get stuck at running the python script and not continue.
