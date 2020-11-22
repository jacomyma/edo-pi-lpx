import mido, math;

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

# Display color
def display(lpx, xy, rgb):
    pad = xy_to_pad_note(xy)
    pad_hex = hex(pad)[2:]
    if len(pad_hex) == 1:
            pad_hex = '0'+pad_hex
    r = hex(math.floor(127*rgb[0]))[2:]
    if len(r) == 1:
        r = '0'+r
    g = hex(math.floor(127*rgb[1]))[2:]
    if len(g) == 1:
        g = '0'+g
    b = hex(math.floor(127*rgb[2]))[2:]
    if len(b) == 1:
        b = '0'+b
    hexmsg = 'F0 00 20 29 02 0C 03 03 '+pad_hex+' '+r+' '+g+' '+b+' F7'
    lpx.send(mido.Message.from_hex(hexmsg))

# Display colors in a series
def display_multi(lpx, data):
    hexmsg = 'F0 00 20 29 02 0C 03 '
    for d in data:
        xy = d[0]
        rgb = d[1]
        pad = xy_to_pad_note(xy)
        pad_hex = hex(pad)[2:]
        if len(pad_hex) == 1:
            pad_hex = '0'+pad_hex
        r = hex(math.floor(127*rgb[0]))[2:]
        if len(r) == 1:
            r = '0'+r
        g = hex(math.floor(127*rgb[1]))[2:]
        if len(g) == 1:
            g = '0'+g
        b = hex(math.floor(127*rgb[2]))[2:]
        if len(b) == 1:
            b = '0'+b
        hexmsg = hexmsg+'03 '+pad_hex+' '+r+' '+g+' '+b+' '
    hexmsg = hexmsg+'F7'
    lpx.send(mido.Message.from_hex(hexmsg))

# Display by velocity code
def display_vel(lpx, xy, vel):
    pad = xy_to_pad_note(xy)
    lpx.send(mido.Message('note_on', channel=0, note=pad, velocity=vel))

# Turn off a pad light
def display_off(lpx, xy):
    pad = xy_to_pad_note(xy)
    lpx.send(mido.Message('note_off', note=pad))

# Reset the display
def display_reset(lpx, displayMenu):
    for pad in pads_midinote:
        lpx.send(mido.Message('note_off', note=pad))
    if displayMenu:
        display_menu(lpx)

# Display menu (button row and column)
def display_menu(lpx):
    global menu
    
    # UI: Exit pad
    display_vel(lpx, menu['exit']['xy'], 60)

    # UI: Settings pad
    display_vel(lpx, menu['settings']['xy'], 102)
    
    # UI: Notes pad
    display_vel(lpx, menu['notes']['xy'], 102)

def display_menu_glow(lpx, xy):
    pad = xy_to_pad_note(xy)
    lpx.send(mido.Message('note_on', channel=2, note=pad, velocity=102))

    
# Menu data
menu = {
    'settings': {'xy': [4,8]},
    'notes': {'xy': [5,8]},
    'exit': {'xy': [7,8]}
}
menu['settings']['note'] = xy_to_pad_note(menu['settings']['xy'])
menu['notes']['note'] = xy_to_pad_note(menu['notes']['xy'])
menu['exit']['note'] = xy_to_pad_note(menu['exit']['xy'])

# Check menu message
def checkMenuMessage(msg):
    if msg.control == menu['exit']['note']:
        return "exit"
    elif msg.control == menu['settings']['note']:
        return "settings"
    elif msg.control == menu['notes']['note']:
        return "notes"
    else:
        return False


# Display text
def display_text(lpx, text, loop):
    if loop:
        loop_hex = '01'
    else:
        loop_hex = '00'

    speed = '10'

    text_bin = text.encode(encoding='utf_8')
    text_hex = text_bin.hex()
    
    hexmsg = 'F0 00 20 29 02 0C 07 '+loop_hex+' '+speed+' 00 03 '+text_hex+' F7'
    lpx.send(mido.Message.from_hex(hexmsg))


