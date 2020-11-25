import time, sched, mido, datetime, sys
import xedo, lpxPads as pads, screens, config

def log(msg):
    print('#', msg)
    logfile = open("LPX-log.txt","a")
    logfile.write(str(datetime.datetime.now()) + " " + str(msg) + '\n')
    logfile.close()

log('\n########################################################### RUN')

s = sched.scheduler(time.time, time.sleep)

def runState(state, firstTime, midi_outputs):
    try:
        log("State: "+state)

        # First of all, settle anything happening
        for outport in midi_outputs:
            outport.panic()
            
        # Then change the state    
        if state == 'edo':
            with mido.open_ioport(config.get('launchpad_midi_id')) as lpx:
                switchToProgrammerMode(lpx, True)
                print(config.get('edo'), "EDO")
                
                if firstTime:
                    pads.display_text(lpx, "EDO "+str(config.get("edo")), False)
                else:
                    pads.display_text(lpx, "", False)
                
                # Note: the line below executes the X-EDO script
                # ad libitum, and only returns a value on exit.
                state = xedo.xedo(lpx, midi_outputs)

                s.enter(0, 1, runState, (state, False, midi_outputs,))
                return

        elif state == 'exit':
             with mido.open_ioport(config.get('launchpad_midi_id')) as lpx:
                switchToProgrammerMode(lpx, False)
                
                # Send any message from LPX to everyone else
                for msg in lpx:
                    for outport in midi_outputs:
                        outport.send(msg)
                #return
        else:
            with mido.open_ioport(config.get('launchpad_midi_id')) as lpx:
                switchToProgrammerMode(lpx, True)
                state = screens.setScreen(lpx, midi_outputs, state)

                s.enter(0, 1, runState, (state, False, midi_outputs,))
                return
    except:
        print("Oops!")
        log("ERROR: "+str(sys.exc_info()[0]))
        
        # Crash management:
        for outport in midi_outputs:
            outport.panic()
        #with mido.open_ioport(config.get('launchpad_midi_id')) as lpx:
        #    pads.display_reset(lpx, False)
        #    pads.display_text(lpx, "OOPS: "+str(sys.exc_info()[0]), True)

# Test whether the Launchpad X is connected (iteratively, until it is)
def testLPX(sc):
    try:
        if config.get('launchpad_midi_id') in mido.get_input_names():
            print("Launchpad X connected")
            midi_outputs = getAllOtherMidiOutputs()
            s.enter(0, 1, runState, ("edo", True, midi_outputs,))
            return
        else:
            print("Waiting for Launchpad X...")
            s.enter(3, 1, testLPX, (sc,))
            return
    except:
        print("Oops!")
        log("ERROR: "+str(sys.exc_info()[0]))

def switchToProgrammerMode(lpx, flag):
    try:
        # The reference is in the LPX programmer's manual
        # https://fael-downloads-prod.focusrite.com/customer/prod/s3fs-public/downloads/Launchpad%20X%20-%20Programmers%20Reference%20Manual.pdf
        if flag:
            print("Launchpad X switched to programmer mode")
            switch = mido.Message.from_hex('F0 00 20 29 02 0C 0E 01 F7')
        else:
            print("Launchpad X switched to normal mode")
            switch = mido.Message.from_hex('F0 00 20 29 02 0C 0E 00 F7')
        lpx.send(switch)
    except:
        print("Oops!")
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


# Init
s.enter(0, 1, testLPX, (s,))
s.run()



