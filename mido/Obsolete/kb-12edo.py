import mido;

# Out port
outport = mido.open_output('RK005:RK005 MIDI 1 28:0')

# Build pads
pads = []
for y in range(1,10):
    for x in range(1,10):
        pads.append(x+y*10)

def pad_to_xy(pad):
    return [(pad-11)%10, round((pad-11-(pad-11)%10)/10)]

bottom_left_note = 36 # two octaves below middle C (C2)
row_offset = 5

def pad_to_note(x, y):
    return bottom_left_note + x + row_offset * y

def send_default(pad):
    # Display C notes in pink
    [x,y] = pad_to_xy(pad)
    if x<8 and y<8:
        note = pad_to_note(x, y)
        if note%12 == 0:
            lp.send(mido.Message('note_on', channel=0, note=pad, velocity=94))
        else:
            lp.send(mido.Message('note_off', note=pad))

with mido.open_ioport('Launchpad X:Launchpad X MIDI 2 24:1') as lp:
    # Reset
    for pad in pads:
        lp.send(mido.Message('note_off', note=pad))
    
    # Default state
    for pad in pads:
        send_default(pad)
        
    # Listen to notes
    for msg in lp:
        if msg.type == "note_on":
            [x,y] = pad_to_xy(msg.note)
            note = pad_to_note(x, y)

            # Output
            outnote = msg.copy(note=note)
            outport.send(outnote)
            
            # Launchpad display
            if msg.velocity == 0:
                # equivalent to note off
                for pad in pads:
                    [x,y] = pad_to_xy(pad)
                    if x<8 and y<8:
                        padnote = pad_to_note(x, y)
                        if note == padnote:
                            send_default(pad)
            else:
                for pad in pads:
                    [x,y] = pad_to_xy(pad)
                    if x<8 and y<8:
                        padnote = pad_to_note(x, y)
                        if note == padnote:
                            lp.send(mido.Message('note_on', channel=0, note=pad, velocity=21))
                
