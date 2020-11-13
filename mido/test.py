import time, sched, mido

settings = {
    'launchpad_midi_id': 'Launchpad X:Launchpad X MIDI 2 24:1'
}

s = sched.scheduler(time.time, time.sleep)

def testLPX(sc):
    global lpx
    if settings['launchpad_midi_id'] in mido.get_input_names():
        print("Launchpad X connected")
        with mido.open_ioport(settings['launchpad_midi_id']) as lpx:
            switchToProgrammerMode(lpx)
    else:
        print("Waiting for Launchpad X...")
        s.enter(3, 1, testLPX, (sc,))

def switchToProgrammerMode(lpx):
    # The reference is in the LPX programmer's manual
    # https://fael-downloads-prod.focusrite.com/customer/prod/s3fs-public/downloads/Launchpad%20X%20-%20Programmers%20Reference%20Manual.pdf
    switch = mido.Message.from_hex('F0 00 20 29 02 0C 0E 01 F7')
    lpx.send(switch)
    print("Launchpad X switched to programmer mode")
        
s.enter(0, 1, testLPX, (s,))
s.run()

