# Install Raspberry Pi 4
I followed the classic steps for a headless install.
Enable SSH and the WiFi through my phone at install.
Install VNC from SSH.
Connect through VNC from my computer through my phone's WiFi.

# Install the stuff necessary to a tutorial.
I follow this tutorial: https://www.linuxrouen.fr/wp/programmation/introduction-a-la-programmation-midi-avec-python-mido-et-rtmidi-23805/
I installed:
* Python 3
* IDLE, which is an IDE for Python (recommended in the tuto)
* Python3-Mido from the software store NOTE: not sure that I did that actually
* mido in Python 3 (pip3 install mido). I don't know why both are necessary, but they seem to be.
* Python-RtMidi (pip3 install python-rtmidi)
* VMPK (from the app store), a virtual midi keyboard
* Qsynth/Fluidsynth (qsynth, from the app store, already installed) a virtual synth
* QJackCtl (app store) that is supposed to give Audio top priority
* Patchage (app store) that visualizes what is connected to what

# First test
I have the model:cycles on the midi port of the RK005.
I send a note to it.
In the python console, I use the following lines:
```
>>> import mido
>>> outport = mido.open_output('RK005:RK005 MIDI 1 24:0')
>>> msg = mido.Message('note_on')
>>> msg2 = mido.Message('note_off')
>>> outport.send(msg)
>>> outport.send(msg2)
```
To get the name of the outputs (idem for inputs):
```
print(mido.get_output_names())
```

Note: when I retried, the RK005 output had a different reference:
'RK005:RK005 MIDI 1 28:0'

# Second try
Options in note messages:

```
>>> import mido
>>> outport = mido.open_output('RK005:RK005 MIDI 1 28:0')
>>> msg = mido.Message('note_on', note=100)
>>> msg2 = mido.Message('note_off', note=100)
>>> outport.send(msg)
>>> outport.send(msg2)
```

