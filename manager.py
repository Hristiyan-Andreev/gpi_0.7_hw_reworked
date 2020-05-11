import os
import subprocess as subp
# import click as cl
# import PyInquirer as pyq

# TODO: Master script to 
# 1) start/stop/restart the main.py
# 2) enable/disable autostart
# 3) Show output and logs
# 4) monitor (health check) the main script

# def check_status_main():
#     this_pid = os.getpid()
#     python_pids = get_pid('python3')
def get_pid(name):
    return list(map(int,subp.check_output(["pidof", "-c", name]).split()))


#-- Test pgrep
this_pid = os.getpid()
print(this_pid)

python_pids = get_pid('python3')
main_py_pids = list(map(int,subp.check_output(["pgrep", "-f", "main.py"]).split()))
print(python_pids)
print(main_py_pids)

python_main_py_pid = set(python_pids).intersection(main_py_pids)
print(python_main_py_pid)

while(True):
    pass

# -- Start the main program from this process -- 
# inp = input("Start the bloody program!")
# process = subp.Popen(['python3','main.py'], stdout=subp.PIPE)
# print(process.communicate())
