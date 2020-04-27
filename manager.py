import os
import subprocess as subp
# import click as cl
# import PyInquirer as pyq


inp = input("Start the bloody program!")
process = subp.Popen(['python3','main.py'], stdout=subp.PIPE)
print(process.communicate())
