import mido, lpxPads as pads;

def setScreen(settings, lpx, outports, screen):
    # Reset
    pads.display_reset(lpx, False)

    # Display menu glow
    if screen == 'notes':
        pads.display_menu_glow(lpx, pads.menu['notes']['xy'])
    elif screen == 'settings':
        pads.display_menu_glow(lpx, pads.menu['settings']['xy'])
        
    # Test
    pads.display_vel(lpx, [4,4], 56)

    # Listen to notes
    for msg in lpx:
        if msg.type == "control_change":
            if msg.value == 0:
                if msg.control == pads.menu[screen]['note']:
                    return 'edo'
