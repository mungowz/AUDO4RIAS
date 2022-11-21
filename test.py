from tkinter import *
import subprocess, shlex

command = "xterm -xrm 'XTerm.vt100.allowTitleOps: false' -T whatever -e python3 performDocking.py"
args = shlex.split(command)
print(args)

subprocess.Popen(args)