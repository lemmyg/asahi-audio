## Testing Asahi Linux userspace audio configuration on 16,1 T2 Mac.

Thanks to chadmed and Asahi Linux.

The project has been adjusted to test Asahi Linux audio workflow on a MacBook Pro 16,1 2019 with T2 audio driver.

New FIRs were created measuring the MacBook Pro 16,1 with UMIK-1 mic and manually created FIRs of EQ filters using REW.

For more information please visit the original project at [asahi-audio](https://github.com/chadmed/asahi-audio)

## Installation instructions

First follow [t2-audio](https://wiki.t2linux.org/guides/audio-config) instructions and install pipewire.

Once the audio is working, you can install the FIRs config in your system.
Note that this configuration has been tested only on Ubuntu 22.04.

Install the following dependecies:
```sh
sudo apt install pipewire pipewire-pulse wireplumber lsp-plugins calf-plugins
```
clone the git branch and install the FIRs config:
```sh
git clone -b macbookT2_16_1 https://github.com/lemmyg/asahi-audio.git
cd asahi-audio
bash mac-audio
```

## Uninstallation
```sh
sudo rm /etc/pipewire/pipewire.conf.d/10-*-sink.conf
sudo rm -r /usr/share/pipewire/devices/apple
```


### Disclaimer
This project has been create to share the settings with [T2 kernel team](https://wiki.t2linux.org/). Note that the project is still under working in progress and may not be safe for general usage. Misconfigured settings in userspace could damage speakers permanently.

Thanks