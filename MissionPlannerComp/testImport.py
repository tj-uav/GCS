import sys
sys.path.append("C:/Python27/Lib")
sys.path.append("C:/Python27/Lib/site-packages")
sys.path.append("C:/Users/Srikar/Documents/UAV/interop/client")
import subprocess
import os
print('Start')
subprocess.call(["echo", "HI"], shell=True)
subprocess.call(["which", "python"], shell=True)
subprocess.call(["echo", "DONE"], shell=True)
print('Done')
#from google.protobuf import json_format