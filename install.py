#!/usr/bin/env python3

# SPDX-License-Identifier: MIT
# (C) 2022 James Calligeros


import os
import shutil
import time
import glob
import subprocess

VALID_MODELS = {"MacBookPro16,1": "t2_161"}

def get_system():
    # Get from the system the current model
    p = subprocess.Popen('dmidecode -s system-product-name',  shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr=p.communicate()
    if stderr:
        raise Exception("Following error has been found: {}".format(stderr))
    return stdout.decode('utf-8').strip()
    


def install_pw_conf(system):
    '''
    Since the audio stack is dumb and cannot pick and choose configurations
    for us on the fly, we must install a specific configuration based on the
    user's machine. Luckily, it's all pretty trivial stuff.
    '''
    #clean up the existing config files
    for configPath in glob.glob("/etc/pipewire/pipewire.conf.d/10-*-sink.conf"):
         os.remove(configPath)
    shutil.copy2(f"conf/{system}.conf",
                 f"/etc/pipewire/pipewire.conf.d/10-{system}-sink.conf")
    return


def install_firs(system):
    
    #clean up the existing config files
    shutil.rmtree(f"/usr/share/pipewire/devices/apple")
    shutil.copytree(f"firs/{system}",
                    f"/usr/share/pipewire/devices/apple/{system}")
    return


def main():
    
    model = get_system()
    valid = model in VALID_MODELS
    machine = VALID_MODELS.get(model)
    if not valid:
        print(f"Sorry, the {model} model is not currently supported.")
        exit()
    
    print(f"This machine is a supported {model} model.\n")

    input("Press Enter to continue...")

    print("Installing PipeWire configuration files...\n")
    pwret = install_pw_conf(machine)
    if pwret == -1:
        print("Could not install PipeWire configuration files.")
        print("This program will now exit.")
        exit()

    print("Installing Finite Impulse Responses...\n")
    irret = install_firs(machine)
    if irret == -1:
        print("Could not install FIRs.")
        print("This program will now exit.")
        exit()


    print("Please put the current built-in audio device into the Pro Audio")
    print("profile. Do not continue until you have done this.")
    input("Press Enter to continue...\n")

    print("Killing PipeWire...\n")
    os.system("killall pipewire")
    time.sleep(2)

    print("PipeWire has been stopped. Please reboot your machine for the")
    print("changes to take effect. Logging out and logging in again is not")
    print("sufficient.")

if __name__ == "__main__":
    main()
