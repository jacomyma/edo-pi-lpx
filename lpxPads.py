import mido, math;
import config

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

    # Octave offset UP / DOWN + Edonote offset LEFT / RIGHT
    oo = config.get('octave_offset')
    vrange = 6
    up = min(vrange, max(0, vrange-oo))/vrange
    dn = min(vrange, max(0, vrange+oo))/vrange
    eo = config.get('edonote_offset')
    hrange = config.get('edo')
    l = min(hrange, max(0, hrange+eo))/hrange
    r = min(hrange, max(0, hrange-eo))/hrange
    
    display_multi(lpx, [
        [[0,8], [0.2*up*up*up*up*up*up, 0.6*up*up*up*up*up, 0.2+0.8*up*up]],   # UP
        [[1,8], [0.2*dn*dn*dn*dn*dn*dn, 0.6*dn*dn*dn*dn*dn, 0.2+0.8*dn*dn]],   # DOWN
        [[2,8], [0.2+0.6*l*l, 0.2*l*l*l*l*l, 0.9*l*l*l*l*l*l]],   # LEFT
        [[3,8], [0.2+0.6*r*r, 0.2*r*r*r*r*r, 0.9*r*r*r*r*r*r]],   # RIGHT
    ])
    
    
def display_menu_glow(lpx, xy):
    pad = xy_to_pad_note(xy)
    lpx.send(mido.Message('note_on', channel=2, note=pad, velocity=102))

    
# Menu data
menu = {
    'settings': {'xy': [4,8]},
    'notes': {'xy': [5,8]},
    'exit': {'xy': [7,8]},
    'UP': {'xy': [0,8]},
    'DOWN': {'xy': [1,8]},
    'LEFT': {'xy': [2,8]},
    'RIGHT': {'xy': [3,8]},
}
for k in menu.keys():
    menu[k]['note'] = xy_to_pad_note(menu[k]['xy'])

# Check menu message
def checkMenuMessage(lpx, msg):
    if   msg.control == menu['exit']['note']:
        return "exit"
    elif msg.control == menu['settings']['note']:
        return "settings"
    elif msg.control == menu['notes']['note']:
        return "notes"
    elif msg.control == menu['UP']['note']:
        config.set('octave_offset', min(6, config.get('octave_offset')+1))
        display_menu(lpx)
        return False
    elif msg.control == menu['DOWN']['note']:
        config.set('octave_offset', max(-6, config.get('octave_offset')-1))
        display_menu(lpx)
        return False
    elif msg.control == menu['LEFT']['note']:
        config.set('edonote_offset', max(-config.get('edo'), config.get('edonote_offset')-1))
        return False
    elif msg.control == menu['RIGHT']['note']:
        config.set('edonote_offset', min(config.get('edo'), config.get('edonote_offset')+1))
        return False
    else:
        return False


# Display text
def display_text(lpx, text, loop):
    if text == "":
        hexmsg = 'F0 00 20 29 02 0C 07 F7'
    else:
        if loop:
            loop_hex = '01'
        else:
            loop_hex = '00'

        speed = '15'

        text_bin = str(text).encode(encoding='utf_8')
        text_hex = text_bin.hex()
        
        hexmsg = 'F0 00 20 29 02 0C 07 '+loop_hex+' '+speed+' 00 03 '+text_hex+' F7'
    lpx.send(mido.Message.from_hex(hexmsg))


# Ratio colors
def getRatioRGB(ratio, f):
    if ratio == "2/1":
        return [f*227/255, f*143/255, f*217/255]
    elif ratio == "3/2":
        return [f*  0/255, f*195/255, f*170/255]
    elif ratio == "4/3":
        return [f*153/255, f*182/255, f* 89/255]
    elif ratio == "5/3":
        return [f*  0/255, f*188/255, f*238/255]
    elif ratio == "5/4":
        return [f*204/255, f*166/255, f* 78/255]
    elif ratio == "6/5":
        return [f*230/255, f*154/255, f* 90/255]
    elif ratio == "7/4":
        return [f* 39/255, f*180/255, f*255/255]
    elif ratio == "7/5":
        return [f*107/255, f*187/255, f*116/255]
    elif ratio == "7/6":
        return [f*240/255, f*146/255, f*103/255]
    elif ratio == "8/5":
        return [f*  0/255, f*193/255, f*222/255]
    elif ratio == "8/7":
        return [f*250/255, f*141/255, f*117/255]
    elif ratio == "9/5":
        return [f*110/255, f*171/255, f*255/255]
    elif ratio == "9/7":
        return [f*184/255, f*173/255, f* 78/255]
    elif ratio == "9/8":
        return [f*254/255, f*138/255, f*127/255]
    elif ratio == "10/7":
        return [f* 82/255, f*191/255, f*131/255]
    elif ratio == "10/9":
        return [f*255/255, f*136/255, f*137/255]
    elif ratio == "12/7":
        return [f*  0/255, f*184/255, f*254/255]
