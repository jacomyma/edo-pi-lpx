# EDO + Raspberry Pi + Launchpad X

## Fresh Raspberry Pi install
*(skip if you have one)*

1.	Build a fresh image of the default Raspbian on the micro SD card.
		If you want to control the Raspberry Pi at a distance, see below.
		Else, you can just put the micro SD card in the Raspberry Pi, and boot it.

2.	These steps are relevant if you want to control the Raspberry headless, from another computer.
		In short, we enable SSH and connect via command line to setup a VNC connection, from which we can see and control the desktop from another computer.

	2.a.	Enable the Wifi by creating a valid wpa_supplicant.conf filr
				-> check https://www.raspberrypi.org/documentation/configuration/wireless/headless.md
	2.b.	Enable SSH by creating a file just named "SSH" in the boot folder
				-> check https://www.tomshardware.com/reviews/raspberry-pi-headless-setup-how-to,6028.html
	2.c.	Put the card into the Raspberry Pi, switch it on (i.e. plug it), and wait until it connects your wifi
	2.d.	Find its IP, you will need it.
				I found the easiest way to be the FING app on a smartphone.
				-> check https://howchoo.com/pi/find-your-raspberry-pis-ip-address
	2.e.	Get a SSH client it you don't have one already. On Windows, I use Putty.
	2.f.	Connect to your raspberry via SSH. Enter the IP address and connect to it. The login is "pi" and the password "raspberry".
	2.g.	Enter ```sudo raspi-config``` to enter the config interface.
				Select "5 Interfacing options"
				Select "P3 VNC"
				Select "<YES>" and hit enter
				Navigate to "<FINISH>" and hit enter
				VNC is now enabled on the Raspberry.
				-> check https://www.tomshardware.com/reviews/raspberry-pi-headless-setup-how-to,6028.html
	2.h.	Download and install VNC on your computer. Create a new connection using the raspberry IP.

				```sudo raspi-config```
				7 Advanced options
				A5 Resolution
				DMT Mode 82 1920x1080 60Hz 16:9
				<FINISH>
				Would you like to reboot now? -> <YES>
				...wait until it reboots and reconnects to the wifi...
				Now it should work

3.	Since this is your first connection, the Raspberry needs a number of things (update etc.)
		Just follow the steps. Nothing unusual, you don't have much to do. It's long, though.
		Just a warning: if you change the password and then try to connect from VNC, think of updating the password in VNC too.

## Install EDO-PI-LPX

4.	Clone this repository:
		Open a terminal, and clone the respository from GitHub by using this line:
		```git clone https://github.com/jacomyma/edo-pi-lpx.git```
		(or whatever the URL of this repository is)
		This will install the code in a repository located at ```/home/pi/edo-pi-lpx```

5.	Install dependencies
		Install mido: ```pip3 install mido```
		Install rt-midi: ```pip3 install python-rtmidi```

6.	Configure for your Launchpad X.
		Basically, we just need to find the Launchpad X's proper identifier.

		6.a.	Plug the Launchpad X and wait until it switches on.

		6.b.	Open a python shell in a terminal, and get the ids of all midi things connected. It goes this way:
					```
					python3
					>>> import mido
					>>> mido_get_input_names()
					[It inputs some list]
					>>> exit()
					```

					Look at the list. The Launchpad X should feature twice (because it has 2 distinct connection; only the second one is useful here). Copy the text of the second connection. For me it looks like this, but the numbers may change:
					```Launchpad X:Launchpad X MIDI 2 28:1```

		6.c.	Update the config. In the folder where you installed the script, presumably ```/home/pi/edo-pi-lpx```, there is a default config file named ```config_default.ini```. Open it in a text editor (right-click > Text editor).
					At the top of the file there is a line with:
					```launchpad_midi_id = Launchpad X:Launchpad X MIDI 2 28:1```
					Replace the right part with the path that you have just obtained, if it differs.

					**NOTE: if you have tried to run the script before, a new file named ```config.ini``` has been generated. In that case, update that file too.**

					**NOTE: at this point you may just try the script for test purpose. Open a new terminal, browse to the repository with ```cd edo-pi-lpx/``` and type ```python3 run.py```. Exit with *CTRL+C*.**

7.	Enable the code on boot:
		In a nutshell, we add a line of code to execute the script on boot.
		But since it's the first time we run ```crontab``` it's going to configure

	7.a.	Open the cron tab by typing, in a terminal:
				```crontab -e```
				-> Since it's the first time, it asks which editor to use. Pick the first.

	7.b.	Add the following line at the end of the file:
				```@reboot sleep 10 && python3 /home/pi/edo-pi-lpx/run.py```
				(if you have used another path, update the line above)

	7.c.	Exit the editor, save when prompted to.
				The script is now installed, you can shut the Raspberry Pi down.

## How to use
Starting with the Raspberry Pi unpowered:
* Plug the Launchpad X. I recomment the USB 3.0 ports (blue)
* Plug the other midi devices (e.g. ContinuuMini, Modal Skulpt...)
* Power the Raspberry Pi
* The Launchpad X will switch on, but keep waiting until its says "EDO-PI". You can then use it.

## Usage
TODO (UI)
