import mido, lpxPads as pads;

def setScreen(settings, lpx, outports, screen):
    global submenu
    # Reset
    pads.display_reset(lpx, False)

    # Display menu glow + set submenu
    if screen == 'notes':
        pads.display_menu_glow(lpx, pads.menu['notes']['xy'])
        submenu = 'edo'
    elif screen == 'settings':
        pads.display_menu_glow(lpx, pads.menu['settings']['xy'])
        submenu = 'settings-1'

    initSubmenu(lpx)
    
    # Listen to notes
    for msg in lpx:
        if msg.type == "control_change":
            if msg.value == 0:
                if msg.control == pads.menu[screen]['note']:
                    return 'edo'

def initSubmenu(lpx):
    if submenu == 'edo':
        #pads.display(lpx, [2,7], [1,0,0])
        rgb_low = [0.2,0.2,0.2]
        rgb_12  = [0.20,0.05,0.30]
        pads.display_multi(lpx, [
            [[2,7], rgb_low],   # EDO 03
            [[3,7], rgb_low],   # EDO 04
            [[4,7], rgb_low],   # EDO 05
            [[5,7], rgb_low],   # EDO 06
            [[6,7], rgb_low],   # EDO 07
            [[7,7], rgb_low],   # EDO 08
            [[0,6], rgb_low],   # EDO 09
            [[1,6], rgb_low],   # EDO 10
            [[2,6], rgb_low],   # EDO 11
            [[3,6], rgb_12 ],   # EDO 12
            [[4,6], rgb_low],   # EDO 13
            [[5,6], rgb_low],   # EDO 14
            [[6,6], rgb_low],   # EDO 15
            [[7,6], rgb_low],   # EDO 16
            [[0,5], rgb_low],   # EDO 17
            [[1,5], rgb_low],   # EDO 18
            [[2,5], rgb_low],   # EDO 19
            [[3,5], rgb_low],   # EDO 20
            [[4,5], rgb_low],   # EDO 21
            [[5,5], rgb_low],   # EDO 22
            [[6,5], rgb_low],   # EDO 23
            [[7,5], rgb_low],   # EDO 24
            [[0,4], rgb_low],   # EDO 25
            [[1,4], rgb_low],   # EDO 26
            [[2,4], rgb_low],   # EDO 27
            [[3,4], rgb_low],   # EDO 28
            [[4,4], rgb_low],   # EDO 29
            [[5,4], rgb_low],   # EDO 30
            [[6,4], rgb_low],   # EDO 31
            [[7,4], rgb_low],   # EDO 32
            [[0,3], rgb_low],   # EDO 33
            [[1,3], rgb_low],   # EDO 34
            [[2,3], rgb_low],   # EDO 35
            [[3,3], rgb_low],   # EDO 36
            [[4,3], rgb_low],   # EDO 37
            [[5,3], rgb_low],   # EDO 38
            [[6,3], rgb_low],   # EDO 39
            [[7,3], rgb_low],   # EDO 40
            [[0,2], rgb_low],   # EDO 41
            [[1,2], rgb_low],   # EDO 42
            [[2,2], rgb_low],   # EDO 43
            [[3,2], rgb_low],   # EDO 44
            [[4,2], rgb_low],   # EDO 45
            [[5,2], rgb_low],   # EDO 46
            [[6,2], rgb_low],   # EDO 47
            [[7,2], rgb_low],   # EDO 48
            [[0,1], rgb_low],   # EDO 49
            [[1,1], rgb_low],   # EDO 50
            [[2,1], rgb_low],   # EDO 51
            [[3,1], rgb_low],   # EDO 52
            [[4,1], rgb_low],   # EDO 53
            [[5,1], rgb_low],   # EDO 54
            [[6,1], rgb_low],   # EDO 55
            [[7,1], rgb_low],   # EDO 56
            [[0,0], rgb_low],   # EDO 57
            [[1,0], rgb_low],   # EDO 58
            [[2,0], rgb_low],   # EDO 59
            [[3,0], rgb_low],   # EDO 60
            [[4,0], rgb_low],   # EDO 61
            [[5,0], rgb_low],   # EDO 62
            [[6,0], rgb_low],   # EDO 63
            [[7,0], rgb_low],   # EDO 64
        ])
        pads.display_text(lpx, 'EDO', False)
        
