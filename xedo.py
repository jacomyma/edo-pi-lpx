import mido, lpxPads as pads, config;

# Note: I use the term "edonote" to refer to edo-specific note notation.
# Edo means "Equal division of octave".
# In fact, an edonote is not even a note. It only relates to the grid display.
# An edonote translates to an actual note given a root pitch.
# The edonote 0 equals the root pitch. The root pitch typically equals the middle C.
# In an edo of X, the edonote X equals to one octave above the root pitch.
# The edonote -X equals to one octave below the root pitch.

def display_default(xy, lpx):
    # Display root edonotes in pink
    edonote = xy_to_edonote(xy)
    [key_12edo, pitch_correction] = edonote_to_12edo(edonote)
    if key_12edo < 0 or key_12edo > 127:
        pads.display_vel(lpx, xy, 121)
    elif edonote%config.get('edo') == 0:
        pads.display_vel(lpx, xy, 94)
    else:
        pads.display_off(lpx, xy)

def xy_to_edonote(xy):
    if config.get('edo') * 127 / 12 > 64:
        bottomleft = -2*config.get('edo') # bottom-left note
    else:
        bottomleft = -27 #_12edo_to_edonote(64)-32
    [x,y] = xy
    return bottomleft + x + config.get('row_offset') * y

def edonote_to_12edo(edonote):
    octaves_offset = edonote/config.get('edo')
    semitones_offset = octaves_offset*12
    key_offset = round(semitones_offset)
    key_correction = semitones_offset - key_offset
    key_12edo = config.get('root_note') + key_offset
    pitch_correction = round(8191 * key_correction / config.get('pitch_bend_range_semitones'))
    return [key_12edo, pitch_correction]
    
# Note: channels 1 and 16 should not be used, as they are
# considered master, which means their values, including pitch,
# apply to all.
round_robin = {
    "allowed_channels": [
        config.get("send_channel_01"),
        config.get("send_channel_02"),
        config.get("send_channel_03"),
        config.get("send_channel_04"),
        config.get("send_channel_05"),
        config.get("send_channel_06"),
        config.get("send_channel_07"),
        config.get("send_channel_08"),
        config.get("send_channel_09"),
        config.get("send_channel_10"),
        config.get("send_channel_11"),
        config.get("send_channel_12"),
        config.get("send_channel_13"),
        config.get("send_channel_14"),
        config.get("send_channel_15"),
        config.get("send_channel_16"),
    ],
    "edonotes": [
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None
    ],
    "current": 15,
}

def play_edonote(msg, edonote, round_robin, outports):
    # Compute note and pitch for edonote
    [key_12edo, pitch_correction] = edonote_to_12edo(edonote)
        
    if key_12edo < 0 or key_12edo > 127:
        return
        
    # Manage round robin for channels
    endnote = msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0)
    newnote = msg.type == 'note_on' and not endnote
    if endnote:
        # Find channels using this edonote
        for chan in range(0,15):
            allowed = round_robin['allowed_channels'][chan]
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
            allowed = round_robin['allowed_channels'][chan]
            chan_edonote = round_robin['edonotes'][chan]
            if allowed and (chan_edonote == None):
                target_chan = chan
                break
        if target_chan == None:
            for i in range(1,17):
                chan = (round_robin['current']+i)%16
                allowed = round_robin['allowed_channels'][chan]
                if allowed:
                    target_chan = chan
                    break
            # Since we override a channel, we send a note_off message
            [old_key_12edo, old_pitch_correction] = edonote_to_12edo(round_robin['edonotes'][target_chan])
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

def send_aftertouch(msg, edonote, round_robin, outports):
    # Compute note and pitch for edonote
    [key_12edo, pitch_correction] = edonote_to_12edo(edonote)
    
    if key_12edo < 0 or key_12edo > 127:
        return
    
    # Manage round robin for channels
    endnote = msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0)
    newnote = msg.type == 'note_on' and not endnote
    
    # Find channels using this edonote
    for chan in range(0,15):
        allowed = round_robin['allowed_channels'][chan]
        chan_edonote = round_robin['edonotes'][chan]
        if allowed and (chan_edonote == edonote):
            # Send aftertouch
            aftertouch = mido.Message('aftertouch')
            aftertouch.channel = chan
            aftertouch.value = msg.value
            aftertouch.time = msg.time
            for outport in outports:
                outport.send(aftertouch)

def xedo(lpx, outports):
    # Reset
    pads.display_reset(lpx, True)
    
    # Default state
    for xy in pads.pads_xy:
        if xy[0]<8 and xy[1]<8:
            display_default(xy, lpx)
    
    # Listen to notes
    for msg in lpx:
        if msg.type == "note_on":
            msg_xy = pads.pad_note_to_xy(msg.note)
            msg_edonote = xy_to_edonote(msg_xy)
            
            # Output
            play_edonote(msg, msg_edonote, round_robin, outports)
            
            # Launchpad display
            if msg.velocity == 0:
                # equivalent to note off
                for xy in pads.pads_xy:
                    if xy[0]<8 and xy[1]<8:
                        edonote = xy_to_edonote(xy)
                        if msg_edonote == edonote:
                            display_default(xy, lpx)
            else:
                for xy in pads.pads_xy:
                    if xy[0]<8 and xy[1]<8:
                        edonote = xy_to_edonote(xy)
                        if msg_edonote == edonote:
                            pads.display_vel(lpx, xy, 21)

        elif msg.type == "polytouch":
            msg_xy = pads.pad_note_to_xy(msg.note)
            msg_edonote = xy_to_edonote(msg_xy)
            send_aftertouch(msg, msg_edonote, round_robin, outports)
        
        elif msg.type == "control_change":
            if msg.value == 0:
                check = pads.checkMenuMessage(msg)
                if check != False:
                    return check

