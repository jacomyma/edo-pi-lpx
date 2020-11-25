# EDO + Raspberry Pi + Launchpad X

## Get a fresh Raspberry Pi

*(skip if you have one)*

### 1. Install fresh Raspberry Pi

Build a fresh image of the default Raspbian on the micro SD card.

More info: https://www.raspberrypi.org/documentation/installation/installing-images/

*If you want to control the Raspberry Pi at a distance, see below. Else, you can just put the micro SD card in the Raspberry Pi, and boot it.*

### 2. Headless install

These steps are relevant if you want to control the Raspberry headless, from another computer. If you prefer plugging a keyboard, mouse and screen, skip this.

In short, we enable SSH and connect via command line to setup a VNC connection, from which we can see and control the desktop from another computer.

#### 2.a. Enable the Wifi
Create a valid ```wpa_supplicant.conf``` file.

More info: https://www.raspberrypi.org/documentation/configuration/wireless/headless.md

#### 2.b. Enable SSH
Creating a file just named ```SSH``` in the boot folder.

More info: https://www.tomshardware.com/reviews/raspberry-pi-headless-setup-how-to,6028.html

#### 2.c. Put the card into the Raspberry Pi, switch it on (i.e. plug it), and wait until it connects your wifi

#### 2.d. Find its IP, you will need it

I found the easiest way to be the FING app on a smartphone.

Also check: https://howchoo.com/pi/find-your-raspberry-pis-ip-address

#### 2.e. Get a SSH client it you don't have one already

On Windows, I use Putty.

#### 2.f. Connect to your raspberry via SSH

For instance, using Putty. Enter the IP address and connect to it. The login is "pi" and the password "raspberry".

#### 2.g. Configure the Raspberry Pi.
* Enter ```sudo raspi-config``` to enter the config interface.
* Select ```5 Interfacing options```
* Select ```P3 VNC```
* Select ```<YES>``` and hit ENTER
* Navigate to ```<FINISH>``` and hit ENTER

VNC is now enabled on the Raspberry.

More info: https://www.tomshardware.com/reviews/raspberry-pi-headless-setup-how-to,6028.html

#### 2.h. Download and install VNC on your computer.

Then create a new connection using the raspberry IP.

##### In case of screen issue

When I tried this, VNC could not display the screen of the Raspberry. There is a fix to that. We can change the resolution in the config.
* Again, enter ```sudo raspi-config``` from the SSH connection.
* Select ```7 Advanced options```
* Select ```A5 Resolution```
* Select ```DMT Mode 82 1920x1080 60Hz 16:9``` (or try another one)
* Select ```<FINISH>``` and hit ENTER
* When asked ```Would you like to reboot now?``` chose ```<YES>```
* ...wait until it reboots and reconnects to the wifi...
* Now it should work.

### 3. Since this is your first connection, the Raspberry needs a number of things

These things are language configuration, updates etc.
Just follow the steps. Nothing unusual, you don't have much to do. It's long, though.
Just a warning: if you change the password and then try to connect from VNC, think of updating the password in VNC too.

## Install EDO-PI-LPX

### 4. Clone this repository

Open a terminal, and clone the respository from GitHub by using this line:
```
git clone https://github.com/jacomyma/edo-pi-lpx.git
```
(or whatever the URL of this repository is)
This will install the code in a repository located at ```/home/pi/edo-pi-lpx```.

### 5. Install dependencies
Install mido:
```
pip3 install mido
```

Install rt-midi:
```
pip3 install python-rtmidi
```

### 7. Enable the code on boot

In a nutshell, we add a line of code to execute the script on boot. But since it's the first time we run ```crontab``` it's going to configure.

#### 7.a. Open the cron tab
Type in a terminal:
```
crontab -e
```
Since it's the first time, it asks which editor to use. Pick the first one.

#### 7.b. Add the following line at the end of the file:
```
@reboot sleep 12 && cd /home/pi/edo-pi-lpx && python3 run.py
```

(if you have used another path, update the line above)

#### 7.c. Exit the editor, save when prompted to.

The script is now installed, you can shut the Raspberry Pi down.

## How to use
Starting with the Raspberry Pi unpowered:
* Plug the Launchpad X. I recomment the USB 3.0 ports (blue)
* Plug the other midi devices (e.g. ContinuuMini, Modal Skulpt...)
* Power the Raspberry Pi
* The Launchpad X will switch on, but keep waiting until its says "EDO-PI". You can then use it.

## Usage
TODO (UI)
