import json
import subprocess

def parse_config(config, parameters):
    with open(config) as f:
        kwargs = json.load(f)
        for param in parameters:
            if not kwargs.get(param):
                kwargs[param] = None
        return kwargs

def run_subprocess(command):
    process = subprocess.Popen(command,
        stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if process.poll() is not None:
            break
        if output:
            print (output.strip().decode("utf-8"))
    retval = process.poll()