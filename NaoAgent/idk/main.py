#!/usr/bin/env python3
import subprocess

def wait_nao_input(){
    python3_command = "python mainNAO.py"  # launch your python2 script

    process = subprocess.Popen(python3_command.split(), stdout=subprocess.PIPE)
}

if __name__ == "__main__":
    
