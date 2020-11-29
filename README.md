# EDO + Raspberry Pi + Launchpad X

## Goal

Use a Launchpad X as a polyphonic, expressive, **microtonal** controller for MPE-compatible hardware synths. No DAW required, but a Raspberry Pi. Can be powered out of a USB power bank for portability. The script creates a configurable [EDO](https://en.xen.wiki/w/EDO) layout just like that:

![General layout](https://github.com/jacomyma/edo-pi-lpx/blob/master/resources/Artboard%2013%20-%2072%20ppi.png?raw=true)

## How to use (in short)

Plug the Launchpad X to the Raspberry Pi where the script has been installed (in the USB 3.0 ports, in blue) and any MPE-compatible USB synth (e.g. Modal Skulpt, ContinuuMini). Power the Raspberry Pi. After a few seconds, the Launchpad X connects to the synth and switches to EDO-PI mode. No interaction with the Raspberry Pi is required. Just power it off after use.

👉 [How to use (complete)](https://github.com/jacomyma/edo-pi-lpx/wiki/How-to-use)

## How to install (in short)

Get a Rapsberry Pi with the default configuration. Download the script on it, and run the few commands required for the installation. That's all.

```
# Download the repository
git clone https://github.com/jacomyma/edo-pi-lpx.git

# Install two dependencies
pip3 install mido
pip3 install python-rtmidi

# Set up the script to run on boot
crontab -e
# Then add the following line to the CRON table:
@reboot sleep 12 && cd /home/pi/edo-pi-lpx && python3 run.py
```

👉 [How to install (complete)](https://github.com/jacomyma/edo-pi-lpx/wiki/How-to-install)

## Disclaimer

I made this project because I wanted a relatively cheap, dawless, portable, polyphonic, expressive and microtonal setup. I did it for myself. I offer it to you without any guarantee that it will actually work, that I will fix your issues, that I will develop it further, or even just maintain it. That being said, the code is quite simple and you're free to take it and bring it further. That would in fact make me super happy! In the meanwhile, I will play music.

## License

The documentation is in CC-BY-SA. The software is in GPL v3.

# Documentation

* [How to install](https://github.com/jacomyma/edo-pi-lpx/wiki/How-to-install)
* [How to use](https://github.com/jacomyma/edo-pi-lpx/wiki/How-to-use) (manual)

---

![Raspberry Pi and Launchpad X](https://github.com/jacomyma/edo-pi-lpx/blob/master/resources/EDO-PI-LPX-photo.jpg?raw=true)
