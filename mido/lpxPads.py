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
