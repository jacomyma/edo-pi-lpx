import mido;

settings = {
    'edo': 9,
    'allowed_channels': [False, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False],
    'row_offset':4,
    'pitch_bend_range_semitones': 96,   # This must match the synth's settings
                                        # Modal Skulpt: 48
                                        # Continuumini: 96
    'root_note': 60 # 60 is the middle C
}

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

# Note: I use the term "edonote" to refer to edo-specific note notation.
# Edo means "Equal division of octave".
# In fact, an edonote is not even a note. It only relates to the grid display.
# An edonote translates to an actual note given a root pitch.
# The edonote 0 equals the root pitch. The root pitch typically equals the middle C.
# In an edo of X, the edonote X equals to one octave above the root pitch.
# The edonote -X equals to one octave below the root pitch.

def display_default(xy, lpx, settings):
    # Display root edonotes in pink
    edonote = xy_to_edonote(xy, settings)
    pad = xy_to_pad_note(xy)
    if edonote%settings['edo'] == 0:
        lpx.send(mido.Message('note_on', channel=0, note=pad, velocity=94))
    else:
        lpx.send(mido.Message('note_off', note=pad))

def xy_to_edonote(xy, settings):
    bottomleft = -2*settings['edo'] # bottom-left note
    [x,y] = xy
    return bottomleft + x + settings['row_offset'] * y

def edonote_to_12edo(edonote, settings):
    octaves_offset = edonote/settings['edo']
    semitones_offset = octaves_offset*12
    key_offset = round(semitones_offset)
    key_correction = semitones_offset - key_offset
    key_12edo = settings['root_note'] + key_offset
    pitch_correction = round(8191 * key_correction / settings['pitch_bend_range_semitones'])
    return [key_12edo, pitch_correction]

# Note: channels 1 and 16 should not be used, as they are
# considered master, which means their values, including pitch,
# apply to all.
round_robin = {
    "edonotes": [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    "current": 15
}

def play_edonote(msg, edonote, round_robin, settings, outports):
    # Compute note and pitch for edonote
    [key_12edo, pitch_correction] = edonote_to_12edo(edonote, settings)
    
    # Manage round robin for channels
    endnote = msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0)
    newnote = msg.type == 'note_on' and not endnote
    if endnote:
        # Find channels using this edonote
        for chan in range(0,15):
            allowed = settings['allowed_channels'][chan]
            chan_edonote = round_robin['edonotes'][chan]
            if allowed and chan_edonote == edonote:
                round_robin['edonotes'][chan] = None

                # Unplay note
                key = msg.copy(channel=chan, note=key_12edo)
                for outport in outports:
                    outport.send(key)

    elif newnote:
        # Find next empty channel
        target_chan = None
        for i in range(1,17):
            chan = (round_robin['current']+i)%16
            allowed = settings['allowed_channels'][chan]
            chan_edonote = round_robin['edonotes'][chan]
            if allowed and (chan_edonote == None):
                target_chan = chan
                break
        if target_chan == None:
            for i in range(1,17):
                chan = (round_robin['current']+i)%16
                allowed = settings['allowed_channels'][chan]
                if allowed:
                    target_chan = chan
                    break
            # Since we override a channel, we send a note_off message
            [old_key_12edo, old_pitch_correction] = edonote_to_12edo(round_robin['edonotes'][target_chan], settings)
            off = mido.Message('note_off', channel=target_chan, note=old_key_12edo)
            for outport in outports:
                outport.send(off)

        round_robin['edonotes'][target_chan] = edonote
        round_robin['current'] = target_chan

        # Play note
        # Pitch correction
        pitch = mido.Message('pitchwheel', channel=target_chan, pitch=pitch_correction)
        for outport in outports:
            outport.send(pitch)
        # Key
        key = msg.copy(note=key_12edo, channel=target_chan)
        for outport in outports:
            outport.send(key)

def send_aftertouch(msg, edonote, round_robin, settings, outports):
    # Compute note and pitch for edonote
    [key_12edo, pitch_correction] = edonote_to_12edo(edonote, settings)
    
    # Manage round robin for channels
    endnote = msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0)
    newnote = msg.type == 'note_on' and not endnote
    
    # Find channels using this edonote
    for chan in range(0,15):
        allowed = settings['allowed_channels'][chan]
        chan_edonote = round_robin['edonotes'][chan]
        if allowed and (chan_edonote == edonote):
            # Send aftertouch
            aftertouch = mido.Message('aftertouch')
            aftertouch.channel = chan
            aftertouch.value = msg.value
            aftertouch.time = msg.time
            for outport in outports:
                outport.send(aftertouch)

def xedo(settings, outports):
    with mido.open_ioport('Launchpad X:Launchpad X MIDI 2 24:1') as lp:
        # Reset
        for pad in pads_midinote:
            lp.send(mido.Message('note_off', note=pad))
        
        # Default state
        for xy in pads_xy:
            if xy[0]<8 and xy[1]<8:
                display_default(xy, lp, settings)
            
        # UI: Exit pad
        exit_pad_note = xy_to_pad_note([7,8])
        lp.send(mido.Message('note_on', channel=0, note=exit_pad_note, velocity=60))
        
        
        # Listen to notes
        for msg in lp:
            if msg.type == "note_on":
                msg_xy = pad_note_to_xy(msg.note)
                msg_edonote = xy_to_edonote(msg_xy, settings)
                
                # Output
                play_edonote(msg, msg_edonote, round_robin, settings, outports)
                
                # Launchpad display
                if msg.velocity == 0:
                    # equivalent to note off
                    for xy in pads_xy:
                        if xy[0]<8 and xy[1]<8:
                            edonote = xy_to_edonote(xy, settings)
                            if msg_edonote == edonote:
                                display_default(xy, lp, settings)
                else:
                    for xy in pads_xy:
                        if xy[0]<8 and xy[1]<8:
                            edonote = xy_to_edonote(xy, settings)
                            if msg_edonote == edonote:
                                pad = xy_to_pad_note(xy)
                                lp.send(mido.Message('note_on', channel=0, note=pad, velocity=21))

            elif msg.type == "polytouch":
                msg_xy = pad_note_to_xy(msg.note)
                msg_edonote = xy_to_edonote(msg_xy, settings)
                send_aftertouch(msg, msg_edonote, round_robin, settings, outports)
            
            elif msg.type == "control_change":
                if msg.value == 0:
                    if msg.control == exit_pad_note:
                        for pad in pads_midinote:
                            lp.send(mido.Message('note_off', note=pad))
                        lp.send(mido.Message('note_on', channel=0, note=exit_pad_note, velocity=0))
                        return "exit"
                    
#xedo(settings)
