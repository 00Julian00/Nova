#Opens 'Interface.py' as a new CMD window

import subprocess
import os

os.chdir(os.path.dirname(os.path.realpath(__file__)) + "\\Interfacing")

subprocess.Popen(["cmd", "/c", "start", "cmd", "/k", f"title Interface && python Interface.py"])