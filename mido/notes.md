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

# Third try: light up the Launchpad
```
>>> lp = mido.open_output('Launchpad X:Launchpad X MIDI 1 24:0')
>>> flashing = mido.Message('note_on', channel=1, note=81, velocity=19)
>>> lp.send(flashing)
```
=> Rien ne se passe T_T
Par contre, si j'exécute ensuite le programme du tuto, là le carré vert clignotant apparaît !!!

# Fourth try
Trying with an io port + close port

```
import mido
lp = mido.open_ioport('Launchpad X:Launchpad X MIDI 1 24:0')
flashing = mido.Message('note_on', channel=1, note=81, velocity=19)
lp.send(flashing)
lp.close()
```
=> Nothing happens T_T
That's because it is the wrong port!!!
This one works:
```
lp = mido.open_ioport('Launchpad X:Launchpad X MIDI 2 24:1')
lp.send(mido.Message('note_on', channel=1, note=81, velocity=19))
# This should flash
lp.send(mido.Message('note_off', channel=1, note=81))
lp.close()
# Back to empty state
```

# 2020-08-02 Attempts at MPE
I want to test a MPE layout for the Launchpad. I do not have a MPE hardware synth right now, so I try to use a software synth.
Config:
My script uses the output named ```Midi Through:Midi Through Port-0 14:0```
In addition, I launch QSynth and in Patchage, I plug the Midi Through port to QSynth.

When I run the script, if I trig a Launchpad key, it lights up a green light in Qsynth. The audio output, however, is mute.

Note: VNC does not support sound anyways. It is however possible to force the sound through headphones, via ```sudo raspi-config``` in advanced options > audio.
I successfully played Youtube videos through headphone audio, but I could not have qSynth work.
I decided to install LMMS (following a recommendation by Sevish) since it comes with ZynAddSubFX. Unfortunately, I could not make it work.
=> it's a failure
I was finally capable of having something that works:
I use qsynth in ALSA configuration (Qsynth > Setup > Audio > Audio driver)
I have to connect the midi input through qjackctl:
```
qjackctl &
qsynth
```

