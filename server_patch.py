#!/usr/bin/env python

# This script will patch your system. Period. No customized end-user bs like in the bash script,
# no nvidia crap you need to worry about, just straight up hypervisor check, upgrade & cfe run.
# I plan on adding other features (maybe), but for now this is it. Deal with it. Oh, and if you don't
# like my code, GFY, it works.
# nh

import subprocess
from pathlib import Path
from time import sleep

# For output trawling, so we can watch wtf is going on. I totally ripped most of this function.
def startPatch(cmd):
    print("\n**** We will now patch this system. Please wait. ****")
    sleep(5)
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)
    print("\n**** Yum run has been completed, packages installed. ****\n")
    cfPull()
    print('\x1b[6;30;42m' + "\n**** Patching has completed!! You might want to REBOOT when you're ready, but I won't force you to! ****\n" + '\x1b[0m')

# Got to do that CFEngine run, there may be a better way like some cf module for some shit but this will work for now
def cfEngine(cmd):
    print("\n**** Now starting the CFEngine run, this could take a while depending on what you need to pull down. ****\n")
    sleep(5)
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)
    print('\x1b[6;30;42m' + "\n**** CFEngine run has completed ****\n" + '\x1b[0m')

def cfPull():
    for path in cfEngine(["/usr/local/bin/runcfengine"]):
        print(path, end="")

# Easiest way to run yum update without having to install the yum module, though we could go that route if I felt like it.
def runThatBih():
    for path in startPatch(["yum", "-y", "update"]):
        print(path, end="")

# Check if system is one of our hypervisors, if it is, give a warning. If not, esskeeettttittt!
virshExist = Path("/usr/bin/virsh")
if virshExist.is_file():
    response = input('\x1b[0;37;41m' + "\n**** This is a HYPERVISOR!! Press 'Y' if you want to continue, press anything else to cancel. ****\n" + '\x1b[0m')
    if response == "Y" :
        print("\n**** You have chosen to continue with patching the hypervisor! ****\n")
        runThatBih()

    else:
        print("\nCanceled. Maybe some other time?\n")
else:

    runThatBih()
