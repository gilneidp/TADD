import commands
import os
import time
import sys

def stop_if_already_running():
        status_pox = 9
	script_name = os.path.basename(__file__)
	l = commands.getstatusoutput("ps aux | grep -e '%s' | grep -v grep | awk '{print $2}'" % "pox.py")
	if l[1]:
		#sys.exit(0);
		status_pox = 1
        else:
		status_pox = 0
        print status_pox
stop_if_already_running()
