import os
import subprocess as subp
# import click as cl
# import PyInquirer as pyq

# TODO: Master script to 
# 1) start/stop/restart the main.py
# 2) enable/disable autostart
# 3) Show output and logs
# 4) monitor (health check) the main script

inp = input("Start the bloody program!")
process = subp.Popen(['python3','main.py'], stdout=subp.PIPE)
print(process.communicate())
