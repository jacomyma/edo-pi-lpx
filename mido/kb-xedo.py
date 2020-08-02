import mido;

# Out port
#outport = mido.open_output('RK005:RK005 MIDI 1 28:0')
outport = mido.open_output('Midi Through:Midi Through Port-0 14:0')

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

# Division of octave
edo=17
row_offset = 7
grid_offset = -2*edo # bottom-left note

# Note: I use the term "edonote" to refer to edo-specific note notation.
# In face, an edonote is not even a note. It only relates to the grid display.
# An edonote translates to an actual note given a root pitch.
# The edonote 0 equals the root pitch. The root pitch typically equals the middle C.
# In an edo of X, the edonote X equals to one octave above the root pitch.
# The edonote -X equals to one octave below the root pitch.

def display_default(xy):
    # Display root edonotes in pink
    edonote = xy_to_edonote(xy)
    pad = xy_to_pad_note(xy)
    if edonote%edo == 0:
        lp.send(mido.Message('note_on', channel=0, note=pad, velocity=94))
    else:
        lp.send(mido.Message('note_off', note=pad))

def xy_to_edonote(xy):
    [x,y] = xy
    return grid_offset + x + row_offset * y

# Playing edo notes
pitch_bend_range_semitones = 2 # This must match the synth's settings
root_note = 60 # 60 is the middle C

def edonote_to_12edo(edonote):
    octaves_offset = edonote/edo
    semitones_offset = octaves_offset*12
    key_offset = round(semitones_offset)
    key_correction = semitones_offset - key_offset
    key_12edo = root_note + key_offset
    pitch_correction = round(8191 * key_correction / pitch_bend_range_semitones)
    return [key_12edo, pitch_correction]
    
round_robin = {
    "allowed_channels": [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True],
    "edonotes": [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
    "current": 0
}

def play_edonote(msg, edonote, round_robin):
    global chan_current, used_channels
    
    # Compute note and pitch for edonote
    [key_12edo, pitch_correction] = edonote_to_12edo(edonote)
    
    # Manage round robin for channels
    endnote = msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0)
    newnote = msg.type == 'note_on' and not endnote
    if endnote:
        # Find channels using this edonote
        for i in range(1,16):
            chan = (round_robin['current']+i)%16
            allowed = round_robin['allowed_channels'][chan]
            chan_edonote = round_robin['edonotes'][chan]
            if allowed and chan_edonote == edonote:
                round_robin['edonotes'][chan] = False

                # Unplay note
                pitch = mido.Message('pitchwheel', channel=chan, pitch=0)
                outport.send(pitch)
                outnote = msg.copy(channel=chan)
                outport.send(outnote)

    elif newnote:
        # Find next empty channel
        target_chan = False
        for i in range(1,16):
            chan = (round_robin['current']+i)%16
            allowed = round_robin['allowed_channels'][chan]
            chan_edonote = round_robin['edonotes'][chan]
            if allowed and not edonote:
                target_chan = chan
                break
        if not target_chan:
            for i in range(1,16):
                chan = (round_robin['current']+i)%16
                allowed = round_robin['allowed_channels'][chan]
                if allowed:
                    target_chan = chan
            [old_key_12edo, old_pitch_correction] = edonote_to_12edo(round_robin['edonotes'][target_chan])
            outport.send(mido.Message('note_off', channel=target_chan, note=old_key_12edo))
            
        round_robin['edonotes'][target_chan] = edonote
        round_robin['current'] = target_chan

        # Play note
        pitch = mido.Message('pitchwheel', channel=target_chan, pitch=pitch_correction)
        outport.send(pitch)
        outnote = msg.copy(note=key_12edo, channel=target_chan)
        outport.send(outnote)
    
with mido.open_ioport('Launchpad X:Launchpad X MIDI 2 24:1') as lp:
    # Reset
    for pad in pads_midinote:
        lp.send(mido.Message('note_off', note=pad))
    
    # Default state
    for xy in pads_xy:
        if xy[0]<8 and xy[1]<8:
            display_default(xy)
        
    # Listen to notes
    for msg in lp:
        if msg.type == "note_on":
            msg_xy = pad_note_to_xy(msg.note)
            msg_edonote = xy_to_edonote(msg_xy)
            
            # Output
            play_edonote(msg, msg_edonote, round_robin)
            
            # Launchpad display
            if msg.velocity == 0:
                # equivalent to note off
                for xy in pads_xy:
                    if xy[0]<8 and xy[1]<8:
                        edonote = xy_to_edonote(xy)
                        if msg_edonote == edonote:
                            display_default(xy)
            else:
                for xy in pads_xy:
                    if xy[0]<8 and xy[1]<8:
                        edonote = xy_to_edonote(xy)
                        if msg_edonote == edonote:
                            pad = xy_to_pad_note(xy)
                            lp.send(mido.Message('note_on', channel=0, note=pad, velocity=21))
                
