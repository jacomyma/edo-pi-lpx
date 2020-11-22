import mido;

# Build pads
pads_midinote = []
for y in range(1,10):
    for x in range(1,10):
        pads_midinote.append(x+y*10)

def pad_note_to_xy(note):
    return [(note-11)%10, round((note-11-(note-11)%10)/10)]

def xy_to_pad_note(xy):
    return 11 + xy[0] + 10*xy[1]

pads_xy = []
for note in pads_midinote:
    pads_xy.append(pad_note_to_xy(note))


# Display

# Display by velocity code
def display_vel(lpx, xy, vel):
    pad = xy_to_pad_note(xy)
    lpx.send(mido.Message('note_on', channel=0, note=pad, velocity=vel))

def display_off(lpx, xy):
    pad = xy_to_pad_note(xy)
    lpx.send(mido.Message('note_off', note=pad))

def display_reset(lpx):
    for pad in pads_midinote:
        lpx.send(mido.Message('note_off', note=pad))
