import time, sched, mido, datetime
import xedo

# SETTINGS

# To know what is the midi identifier of your Launchpad X,
# plug it and use these lines:
# import mido
# mido.get_ioport_names()

# Note: the Launchpad X appears twice.
# Ignore the first instance, which is dedicated to the DAW.
# Use the second MIDI interface.

settings = {
    'launchpad_midi_id': 'Launchpad X:Launchpad X MIDI 2 24:1',
    'allowed_channels': [False, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False],
    'edo': 17,
    'row_offset': 7,
    'pitch_bend_range_semitones': 48,   # This must match the synth's settings
                                        # Modal Skulpt: 48
                                        # Continuumini: 96
    'root_note': 60 # 60 is the middle C
}

def log(msg):
    logfile = open("LPX-log.txt","a")
    logfile.write(str(datetime.datetime.now()) + " " + str(msg))
    logfile.close()

log("#### RUN ####")

s = sched.scheduler(time.time, time.sleep)

def runState(state):
    print("Run",state,"mode")
    if state == 'edo':
        with mido.open_ioport(settings['launchpad_midi_id']) as lpx:
            switchToProgrammerMode(lpx, True)
            print(settings['edo'], "EDO")
            midi_outputs = getAllOtherMidiOutputs()
            # Note: the line below executes the X-EDO script
            # ad libitum, and only returns a value on exit.
            state = xedo.xedo(settings, midi_outputs)
            return runState(state)

    elif state == 'exit':
         with mido.open_ioport(settings['launchpad_midi_id']) as lpx:
            switchToProgrammerMode(lpx, False)
            midi_outputs = getAllOtherMidiOutputs()
            # Send any message from LPX to everyone else
            with mido.open_ioport(settings['launchpad_midi_id']) as lp:
                for msg in lp:
                    for outport in midi_outputs:
                        outport.send(msg)

            #return

# Test whether the Launchpad X is connected (iteratively, until it is)
def testLPX(sc):
    global lpx
    try:
        if settings['launchpad_midi_id'] in mido.get_input_names():
            print("Launchpad X connected")
            runState("edo")
        else:
            print("Waiting for Launchpad X...")
            s.enter(3, 1, testLPX, (sc,))
    except:
        print("Oops!", sys.exc_info()[0])
        log("ERROR: "+str(sys.exc_info()[0]))

def switchToProgrammerMode(lpx, flag):
    try:
        # The reference is in the LPX programmer's manual
        # https://fael-downloads-prod.focusrite.com/customer/prod/s3fs-public/downloads/Launchpad%20X%20-%20Programmers%20Reference%20Manual.pdf
        if flag:
            switch = mido.Message.from_hex('F0 00 20 29 02 0C 0E 01 F7')
        else:
            switch = mido.Message.from_hex('F0 00 20 29 02 0C 0E 00 F7')
        lpx.send(switch)
        print("Launchpad X switched to programmer mode")
    except:
        print("Oops!", sys.exc_info()[0])
        log("ERROR: "+str(sys.exc_info()[0]))

def getAllOtherMidiOutputs():
    # Connect the LPX to all midi outputs
    # (except itself)
    midi_outputs = []
    outputs_str = ''
    for port in mido.get_output_names():
        if 'Launchpad' not in port and 'Through' not in port and 'RtMid' not in port:
            midi_outputs.append(mido.open_output(port))
            outputs_str = outputs_str+'<'+port+'> '
    return midi_outputs

s.enter(0, 1, testLPX, (s,))
s.run()

