# Autoconnect Midi

This repository is basically a walkthrough. It makes my process reproducible.

## Goal
**Setup:**: I Have my Raspberry Pi 4 connected to both my Launchpad X and Continuumini.
**Goal:**
* I want the Launchpad X to send midi to the Continuumini
* I want that to happen every time I plug them

## Principle
Linux has its own MIDI management system called ALSA.
You can get to know the MIDI devices and connect them with command lines.

See what is connected:
```
$ aconnect -i
client 0: 'System' [type=kernel]
    0 'Timer           '
    1 'Announce        '
client 14: 'Midi Through' [type=kernel]
    0 'Midi Through Port-0'
client 20: 'Launchpad X' [type=kernel,card=1]
    0 'Launchpad X MIDI 1'
    1 'Launchpad X MIDI 2'
client 24: 'ContinuuMini SN000220' [type=kernel,card=2]
    0 'ContinuuMini SN000220 MIDI 1'
```
This is the actual result on my setup. Each device has a number, for instance the Launchpad is 20.
Each device can have multiple MIDI ports. The relevant midi port for the Launchpad is the second one (1).
So that input is noted "20:1". Similarly the ContinuuMini is "24:0".

The devices seem to always have the same numbers, but I don't see why it would be the case, so I would not count on it.

I can connect the devices just like that:
```
aconnect 20:1 24:0
```

Now, I would like to have that run every time I just connect the devices.

## Next step
To do
