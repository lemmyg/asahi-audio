#!/usr/bin/env python3

# SPDX-License-Identifier: MIT
# (C) 2022 James Calligeros


import os
import shutil
import time
import glob

def get_system():
    # Use the list of subdirs in 'conf' as our list of supported machines
    supported = os.listdir(path="./conf/")

    # Get rid of '.conf'
    for i, machine in enumerate(supported):
        supported[i] = machine[0:4]

    with open("/sys/firmware/devicetree/base/compatible", "r") as sys:
        sys = sys.read()
        compat = sys[6:10] # Get only the 4 chars after 'apple,'

        if compat in supported:
            return compat
        else:
            return -1


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
    #forcing j316 config
    #machine = get_system()
    machine = "t2_161"
    

    if machine == -1:
        print(f"Sorry, the {machine} is not currently supported.")
        exit()

    print(f"This machine is a {machine}.\n")

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
