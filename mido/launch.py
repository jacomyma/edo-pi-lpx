import mido

# SETTINGS

# To know what is the midi identifier of your Launchpad X,
# plug it and use these lines:
# import mido
# mido.get_ioport_names()

# Note: the Launchpad X appears twice.
# Ignore the first instance, which is dedicated to the DAW.
# Use the second interface.

settings = {
    'launchpad_midi_id': 'Launchpad X:Launchpad X MIDI 2 24:1'
}

def connect():
    global settings
    # Connect the LPX to all midi outputs
    # (except itself)
    midi_outputs = []
    outputs_str = ''
    for port in mido.get_output_names():
        if 'Launchpad' not in port and 'Through' not in port and 'RtMid' not in port:
            midi_outputs.append(mido.open_output(port))
            outputs_str = outputs_str+'<'+port+'> '

    # For test: send anything
    with mido.open_ioport(settings['launchpad_midi_id']) as lp:
        for msg in lp:
            for outport in midi_outputs:
                outport.send(msg)

    # Test whether the LPX is in programmer mode
    # TODO
    
connect()
    
