import schedule
import time
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
    'launchpad_midi_id': 'Launchpad X:Launchpad X MIDI 2 24:1',
    'interval_seconds': 1
}

# MECHANICS

lpxen_out_ports = []
old_outputs_str = ''

def monitor():
    global old_outputs_str, lpxen_out_ports
    midi_outputs = []
    outputs_str = ''
    #for port in mido.get_output_names():
    #    if 'Launchpad' not in port and 'Through' not in port and 'RtMid' not in port:
    #        #midi_outputs.append(mido.open_output(port))
    #        outputs_str = outputs_str+'<'+port+'> '
    print('Outputs:', mido.get_output_names())
    
def monitor2():
    global old_outputs_str, lpxen_out_ports
    # Connect the LPX to all midi outputs
    # (except itself)
    midi_outputs = []
    outputs_str = ''
    for port in mido.get_output_names():
        if 'Launchpad' not in port and 'Through' not in port and 'RtMid' not in port:
            midi_outputs.append(mido.open_output(port))
            outputs_str = outputs_str+'<'+port+'> '
    if outputs_str != old_outputs_str:
        print('New ports detected:', outputs_str)
        lpxen_out_ports = midi_outputs
        old_outputs_str = outputs_str
    else:
        print('No change:', outputs_str)

    # For test: send anything
    with mido.open_ioport('Launchpad X:Launchpad X MIDI 2 24:1') as lp:
        for msg in lp:
            for outport in lpxen_out_ports:
                outport.send(msg)

    # Test whether the LPX is in programmer mode

schedule.every(settings['interval_seconds']).seconds.do(monitor)  

while True:  
    schedule.run_pending()  
    time.sleep(1)
