import mido, lpxPads as pads, config;

def getRatioName(ratio):
    if ratio == "2/1":
        return "Octave"
    elif ratio == "3/2":
        return "Perfect Fifth"
    elif ratio == "4/3":
        return "Perfect Fourth"
    elif ratio == "5/3":
        return "Major Sixth"
    elif ratio == "5/4":
        return "Classic Major Third"
    elif ratio == "6/5":
        return "Classic Minor Third"
    elif ratio == "7/4":
        return "Harmonic Seventh"
    elif ratio == "7/5":
        return "Narrow Tritone"
    elif ratio == "7/6":
        return "Septimal Minor Third"
    elif ratio == "8/5":
        return "Classic Minor Sixth"
    elif ratio == "8/7":
        return "Septimal Major Second"
    elif ratio == "9/5":
        return "Just Minor Seventh"
    elif ratio == "9/7":
        return "Septimal Major Third"
    elif ratio == "9/8":
        return "Whole Tone"
    elif ratio == "10/7":
        return "High Tritone"
    elif ratio == "10/9":
        return "Small Whole Tone"
    elif ratio == "12/7":
        return "Septimal Major Sixth"
        
submenu_notes = 'edo'
submenu_settings = 'settings' # No submenus for the moment
def setScreen(lpx, outports, screen):
    global submenu, submenu_notes, submenu_settings

    # Set initial submenu
    if screen == 'notes':
        submenu = submenu_notes
    elif screen == 'settings':
        submenu = submenu_settings

    initSubmenu(lpx, screen)
    
    # Listen to notes
    for msg in lpx:
        if msg.type == "control_change":
            if msg.value == 0:
                check = pads.checkMenuMessage(lpx, msg)
                if check != False:
                    if check == screen:
                        return "edo"
                    else:
                        return check
                else:
                    # Submenu 1
                    if msg.control == pads.xy_to_pad_note([8, 7]):
                        if screen == 'notes' and submenu != 'edo':
                            submenu = 'edo'
                            submenu_notes = 'edo'
                            initSubmenu(lpx, screen)
                            
                    # Submenu 2
                    elif msg.control == pads.xy_to_pad_note([8, 6]):
                        if screen == 'notes' and submenu != 'row':
                            submenu = 'row'
                            submenu_notes = 'row'
                            initSubmenu(lpx, screen)
                            
                    # Submenu 3
                    elif msg.control == pads.xy_to_pad_note([8, 5]):
                        if screen == 'notes' and submenu != 'color':
                            submenu = 'color'
                            submenu_notes = 'color'
                            initSubmenu(lpx, screen)
                        
        elif msg.type == 'note_on' and msg.velocity > 2:
            xy = pads.pad_note_to_xy(msg.note)
            if submenu == 'edo':
                edo = 1 + xy[0] + 8*(7-xy[1])
                if config.get('help'):
                    pads.display_text(lpx, str(edo), False)
                config.set('edo', edo)
                config.set('octave_offset', 0)
                config.set('edonote_offset', 0)
                displayEdoPads(lpx)
            elif submenu == 'row':
                if xy[1] == 7:
                    row_offset = xy[0]+1
                    if config.get('help'):
                        pads.display_text(lpx, str(row_offset), False)
                    config.set('row_offset', row_offset)
                    displayRowPads(lpx)
            elif submenu == 'color':
                if xy[0] <4:
                    if xy[1] == 7:
                        ratio = "7/6"
                    elif xy[1] == 6:
                        ratio = "5/4"
                    elif xy[1] == 5:
                        ratio = "7/5"
                    elif xy[1] == 4:
                        ratio = "3/2"
                    elif xy[1] == 3:
                        ratio = "5/3"
                    elif xy[1] == 2:
                        ratio = "7/4"
                    elif xy[1] == 1:
                        ratio = "9/5"
                    elif xy[1] == 0:
                        ratio = "9/7"
                else:
                    if xy[1] == 7:
                        ratio = "12/7"
                    elif xy[1] == 6:
                        ratio = "8/5"
                    elif xy[1] == 5:
                        ratio = "10/7"
                    elif xy[1] == 4:
                        ratio = "4/3"
                    elif xy[1] == 3:
                        ratio = "6/5"
                    elif xy[1] == 2:
                        ratio = "8/7"
                    elif xy[1] == 1:
                        ratio = "10/9"
                    elif xy[1] == 0:
                        ratio = "9/8"
                if xy[0] != 3 and xy[0] != 7:
                    val = "Off"
                    if xy[0] == 1 or xy[0] == 5:
                        val = "White"
                    if xy[0] == 2 or xy[0] == 6:
                        val = "Color"
                    if config.get('help'):
                        pads.display_text(lpx, ratio+" "+val, False)
                    config.set(ratio, val)
                    displayColorPads(lpx)
                else:
                    if config.get('help'):
                        pads.display_text(lpx, ratio+" "+getRatioName(ratio), False)
            
            elif submenu == 'settings':
                if (xy[1] == 7 and xy[0]>0) or (xy[1] == 6 and xy[0]<7):
                    channel = str(1 + xy[0] + 8*(7-xy[1]))
                    if len(channel) == 1:
                        channel = "0" + channel
                    chanData = config.get('send_channel_'+channel)
                    if config.get('help'):
                        pads.display_text(lpx, 'Ch.' + channel + (' OFF' if chanData else ' ON'), False)
                    config.set('send_channel_'+channel, chanData==False)
                    displaySettingsPads(lpx)
                elif xy[1] == 4 and xy[0]<4:
                    if xy[0] == 0:
                        pitchRange = 12
                    elif xy[0] == 1:
                        pitchRange = 24
                    elif xy[0] ==3:
                        pitchRange = 96
                    else:
                        pitchRange = 48
                    if config.get('help'):
                        pads.display_text(lpx, str(pitchRange)+" Pitch Range", False)
                    config.set('pitch_bend_range_semitones', pitchRange)
                    displaySettingsPads(lpx)
                elif xy[0] == 7 and xy[1] == 0:
                    config.set('help', not config.get('help'))
                    if config.get('help'):
                        pads.display_text(lpx, "Help ON", False)
                    displaySettingsPads(lpx)
            

def initSubmenu(lpx, screen):
    # Reset
    pads.display_reset(lpx, False)

    # Display menu glow
    if screen == 'notes':
        pads.display_menu_glow(lpx, pads.menu['notes']['xy'])
    elif screen == 'settings':
        pads.display_menu_glow(lpx, pads.menu['settings']['xy'])
    
    if submenu == 'edo':
        if config.get('help'):
            pads.display_text(lpx, 'EDO', False)
        displayEdoSubmenu(lpx)
        displayEdoPads(lpx)
    elif submenu == 'row':
        if config.get('help'):
            pads.display_text(lpx, 'ROW', False)
        displayEdoSubmenu(lpx)
        displayRowPads(lpx)
    elif submenu == 'color':
        if config.get('help'):
            pads.display_text(lpx, 'COLOR', False)
        displayEdoSubmenu(lpx)
        displayColorPads(lpx)
    elif submenu == 'settings':
        if config.get('help'):
            pads.display_text(lpx, 'MPE', False)
        displaySettingsPads(lpx)

def displayEdoSubmenu(lpx):
    rgb_low  = [0.05, 0.15, 0.05]
    rgb_high = [0.60, 1.00, 0.60]
    pads.display_multi(lpx, [
        [[8,7], rgb_high if submenu == 'edo'   else rgb_low],   # Submenu edo
        [[8,6], rgb_high if submenu == 'row'   else rgb_low],   # Submenu row
        [[8,5], rgb_high if submenu == 'color' else rgb_low],   # Submenu color
    ])

def displayEdoPads(lpx):
    rgb_low  = [0.2, 0.2, 0.2]
    rgb_high = [1.0, 1.0, 1.0]
    rgb_12   = [0.3, 0.1, 0.2]
    rgb_12h  = [0.8, 0.2, 1.0]
    pads.display_multi(lpx, [
        [[0,7], rgb_high if config.get('edo')==1  else rgb_low],   # EDO 01
        [[1,7], rgb_high if config.get('edo')==2  else rgb_low],   # EDO 02
        [[2,7], rgb_high if config.get('edo')==3  else rgb_low],   # EDO 03
        [[3,7], rgb_high if config.get('edo')==4  else rgb_low],   # EDO 04
        [[4,7], rgb_high if config.get('edo')==5  else rgb_low],   # EDO 05
        [[5,7], rgb_high if config.get('edo')==6  else rgb_low],   # EDO 06
        [[6,7], rgb_high if config.get('edo')==7  else rgb_low],   # EDO 07
        [[7,7], rgb_high if config.get('edo')==8  else rgb_low],   # EDO 08
        [[0,6], rgb_high if config.get('edo')==9  else rgb_low],   # EDO 09
        [[1,6], rgb_high if config.get('edo')==10 else rgb_low],   # EDO 10
        [[2,6], rgb_high if config.get('edo')==11 else rgb_low],   # EDO 11
        [[3,6], rgb_12h  if config.get('edo')==12 else rgb_12 ],   # EDO 12
        [[4,6], rgb_high if config.get('edo')==13 else rgb_low],   # EDO 13
        [[5,6], rgb_high if config.get('edo')==14 else rgb_low],   # EDO 14
        [[6,6], rgb_high if config.get('edo')==15 else rgb_low],   # EDO 15
        [[7,6], rgb_high if config.get('edo')==16 else rgb_low],   # EDO 16
        [[0,5], rgb_high if config.get('edo')==17 else rgb_low],   # EDO 17
        [[1,5], rgb_high if config.get('edo')==18 else rgb_low],   # EDO 18
        [[2,5], rgb_high if config.get('edo')==19 else rgb_low],   # EDO 19
        [[3,5], rgb_high if config.get('edo')==20 else rgb_low],   # EDO 20
        [[4,5], rgb_high if config.get('edo')==21 else rgb_low],   # EDO 21
        [[5,5], rgb_high if config.get('edo')==22 else rgb_low],   # EDO 22
        [[6,5], rgb_high if config.get('edo')==23 else rgb_low],   # EDO 23
        [[7,5], rgb_high if config.get('edo')==24 else rgb_low],   # EDO 24
        [[0,4], rgb_high if config.get('edo')==25 else rgb_low],   # EDO 25
        [[1,4], rgb_high if config.get('edo')==26 else rgb_low],   # EDO 26
        [[2,4], rgb_high if config.get('edo')==27 else rgb_low],   # EDO 27
        [[3,4], rgb_high if config.get('edo')==28 else rgb_low],   # EDO 28
        [[4,4], rgb_high if config.get('edo')==29 else rgb_low],   # EDO 29
        [[5,4], rgb_high if config.get('edo')==30 else rgb_low],   # EDO 30
        [[6,4], rgb_high if config.get('edo')==31 else rgb_low],   # EDO 31
        [[7,4], rgb_high if config.get('edo')==32 else rgb_low],   # EDO 32
        [[0,3], rgb_high if config.get('edo')==33 else rgb_low],   # EDO 33
        [[1,3], rgb_high if config.get('edo')==34 else rgb_low],   # EDO 34
        [[2,3], rgb_high if config.get('edo')==35 else rgb_low],   # EDO 35
        [[3,3], rgb_high if config.get('edo')==36 else rgb_low],   # EDO 36
        [[4,3], rgb_high if config.get('edo')==37 else rgb_low],   # EDO 37
        [[5,3], rgb_high if config.get('edo')==38 else rgb_low],   # EDO 38
        [[6,3], rgb_high if config.get('edo')==39 else rgb_low],   # EDO 39
        [[7,3], rgb_high if config.get('edo')==40 else rgb_low],   # EDO 40
        [[0,2], rgb_high if config.get('edo')==41 else rgb_low],   # EDO 41
        [[1,2], rgb_high if config.get('edo')==42 else rgb_low],   # EDO 42
        [[2,2], rgb_high if config.get('edo')==43 else rgb_low],   # EDO 43
        [[3,2], rgb_high if config.get('edo')==44 else rgb_low],   # EDO 44
        [[4,2], rgb_high if config.get('edo')==45 else rgb_low],   # EDO 45
        [[5,2], rgb_high if config.get('edo')==46 else rgb_low],   # EDO 46
        [[6,2], rgb_high if config.get('edo')==47 else rgb_low],   # EDO 47
        [[7,2], rgb_high if config.get('edo')==48 else rgb_low],   # EDO 48
        [[0,1], rgb_high if config.get('edo')==49 else rgb_low],   # EDO 49
        [[1,1], rgb_high if config.get('edo')==50 else rgb_low],   # EDO 50
        [[2,1], rgb_high if config.get('edo')==51 else rgb_low],   # EDO 51
        [[3,1], rgb_high if config.get('edo')==52 else rgb_low],   # EDO 52
        [[4,1], rgb_high if config.get('edo')==53 else rgb_low],   # EDO 53
        [[5,1], rgb_high if config.get('edo')==54 else rgb_low],   # EDO 54
        [[6,1], rgb_high if config.get('edo')==55 else rgb_low],   # EDO 55
        [[7,1], rgb_high if config.get('edo')==56 else rgb_low],   # EDO 56
        [[0,0], rgb_high if config.get('edo')==57 else rgb_low],   # EDO 57
        [[1,0], rgb_high if config.get('edo')==58 else rgb_low],   # EDO 58
        [[2,0], rgb_high if config.get('edo')==59 else rgb_low],   # EDO 59
        [[3,0], rgb_high if config.get('edo')==60 else rgb_low],   # EDO 60
        [[4,0], rgb_high if config.get('edo')==61 else rgb_low],   # EDO 61
        [[5,0], rgb_high if config.get('edo')==62 else rgb_low],   # EDO 62
        [[6,0], rgb_high if config.get('edo')==63 else rgb_low],   # EDO 63
        [[7,0], rgb_high if config.get('edo')==64 else rgb_low],   # EDO 64
    ])

def displayRowPads(lpx):
    rgb_low  = [0.2, 0.2, 0.2]
    rgb_high = [1.0, 1.0, 1.0]
    pads.display_multi(lpx, [
        [[0,7], rgb_high if config.get('row_offset')==1  else rgb_low],   # Row Offset 01
        [[1,7], rgb_high if config.get('row_offset')==2  else rgb_low],   # Row Offset 02
        [[2,7], rgb_high if config.get('row_offset')==3  else rgb_low],   # Row Offset 03
        [[3,7], rgb_high if config.get('row_offset')==4  else rgb_low],   # Row Offset 04
        [[4,7], rgb_high if config.get('row_offset')==5  else rgb_low],   # Row Offset 05
        [[5,7], rgb_high if config.get('row_offset')==6  else rgb_low],   # Row Offset 06
        [[6,7], rgb_high if config.get('row_offset')==7  else rgb_low],   # Row Offset 07
        [[7,7], rgb_high if config.get('row_offset')==8  else rgb_low],   # Row Offset 08
    ])

def getRatioRGB(ratio, hl):
    factor = 1 if hl else 0.15
    return pads.getRatioRGB(ratio, factor)

def displayColorPads(lpx):
    rgb_off_low  =   [0.05, 0.00, 0.00]
    rgb_off_high =   [0.80, 0.00, 0.00]
    rgb_white_low  = [0.08, 0.08, 0.08]
    rgb_white_high = [0.90, 0.90, 0.90]
    pads.display_multi(lpx, [
        [[0,7], rgb_off_high              if config.get('7/6') == "Off"   else rgb_off_low               ],   # Ratio 7/6 Off
        [[1,7], rgb_white_high            if config.get('7/6') == "White" else rgb_white_low             ],   # Ratio 7/6 White
        [[2,7], getRatioRGB('7/6', True)  if config.get('7/6') == "Color" else getRatioRGB('7/6', False) ],   # Ratio 7/6 Color
        [[0,6], rgb_off_high              if config.get('5/4') == "Off"   else rgb_off_low               ],   # Ratio 5/4 Off
        [[1,6], rgb_white_high            if config.get('5/4') == "White" else rgb_white_low             ],   # Ratio 5/4 White
        [[2,6], getRatioRGB('5/4', True)  if config.get('5/4') == "Color" else getRatioRGB('5/4', False) ],   # Ratio 5/4 Color
        [[0,5], rgb_off_high              if config.get('7/5') == "Off"   else rgb_off_low               ],   # Ratio 7/5 Off
        [[1,5], rgb_white_high            if config.get('7/5') == "White" else rgb_white_low             ],   # Ratio 7/5 White
        [[2,5], getRatioRGB('7/5', True)  if config.get('7/5') == "Color" else getRatioRGB('7/5', False) ],   # Ratio 7/5 Color
        [[0,4], rgb_off_high              if config.get('3/2') == "Off"   else rgb_off_low               ],   # Ratio 3/2 Off
        [[1,4], rgb_white_high            if config.get('3/2') == "White" else rgb_white_low             ],   # Ratio 3/2 White
        [[2,4], getRatioRGB('3/2', True)  if config.get('3/2') == "Color" else getRatioRGB('3/2', False) ],   # Ratio 3/2 Color
        [[0,3], rgb_off_high              if config.get('5/3') == "Off"   else rgb_off_low               ],   # Ratio 5/3 Off
        [[1,3], rgb_white_high            if config.get('5/3') == "White" else rgb_white_low             ],   # Ratio 5/3 White
        [[2,3], getRatioRGB('5/3', True)  if config.get('5/3') == "Color" else getRatioRGB('5/3', False) ],   # Ratio 5/3 Color
        [[0,2], rgb_off_high              if config.get('7/4') == "Off"   else rgb_off_low               ],   # Ratio 7/4 Off
        [[1,2], rgb_white_high            if config.get('7/4') == "White" else rgb_white_low             ],   # Ratio 7/4 White
        [[2,2], getRatioRGB('7/4', True)  if config.get('7/4') == "Color" else getRatioRGB('7/4', False) ],   # Ratio 7/4 Color
        [[0,1], rgb_off_high              if config.get('9/5') == "Off"   else rgb_off_low               ],   # Ratio 9/5 Off
        [[1,1], rgb_white_high            if config.get('9/5') == "White" else rgb_white_low             ],   # Ratio 9/5 White
        [[2,1], getRatioRGB('9/5', True)  if config.get('9/5') == "Color" else getRatioRGB('9/5', False) ],   # Ratio 9/5 Color
        [[0,0], rgb_off_high              if config.get('9/7') == "Off"   else rgb_off_low               ],   # Ratio 9/7 Off
        [[1,0], rgb_white_high            if config.get('9/7') == "White" else rgb_white_low             ],   # Ratio 9/7 White
        [[2,0], getRatioRGB('9/7', True)  if config.get('9/7') == "Color" else getRatioRGB('9/7', False) ],   # Ratio 9/7 Color

        [[4,7], rgb_off_high              if config.get('12/7') == "Off"   else rgb_off_low               ],   # Ratio 12/7 Off
        [[5,7], rgb_white_high            if config.get('12/7') == "White" else rgb_white_low             ],   # Ratio 12/7 White
        [[6,7], getRatioRGB('12/7', True) if config.get('12/7') == "Color" else getRatioRGB('12/7', False)],   # Ratio 12/7 Color
        [[4,6], rgb_off_high              if config.get('8/5')  == "Off"   else rgb_off_low               ],   # Ratio 8/5 Off
        [[5,6], rgb_white_high            if config.get('8/5')  == "White" else rgb_white_low             ],   # Ratio 8/5 White
        [[6,6], getRatioRGB('8/5', True)  if config.get('8/5')  == "Color" else getRatioRGB('8/5', False) ],   # Ratio 8/5 Color
        [[4,5], rgb_off_high              if config.get('10/7') == "Off"   else rgb_off_low               ],   # Ratio 10/7 Off
        [[5,5], rgb_white_high            if config.get('10/7') == "White" else rgb_white_low             ],   # Ratio 10/7 White
        [[6,5], getRatioRGB('10/7', True) if config.get('10/7') == "Color" else getRatioRGB('10/7', False)],   # Ratio 10/7 Color
        [[4,4], rgb_off_high              if config.get('4/3')  == "Off"   else rgb_off_low               ],   # Ratio 4/3 Off
        [[5,4], rgb_white_high            if config.get('4/3')  == "White" else rgb_white_low             ],   # Ratio 4/3 White
        [[6,4], getRatioRGB('4/3', True)  if config.get('4/3')  == "Color" else getRatioRGB('4/3', False) ],   # Ratio 4/3 Color
        [[4,3], rgb_off_high              if config.get('6/5')  == "Off"   else rgb_off_low               ],   # Ratio 6/5 Off
        [[5,3], rgb_white_high            if config.get('6/5')  == "White" else rgb_white_low             ],   # Ratio 6/5 White
        [[6,3], getRatioRGB('6/5', True)  if config.get('6/5')  == "Color" else getRatioRGB('6/5', False) ],   # Ratio 6/5 Color
        [[4,2], rgb_off_high              if config.get('8/7')  == "Off"   else rgb_off_low               ],   # Ratio 8/7 Off
        [[5,2], rgb_white_high            if config.get('8/7')  == "White" else rgb_white_low             ],   # Ratio 8/7 White
        [[6,2], getRatioRGB('8/7', True)  if config.get('8/7')  == "Color" else getRatioRGB('8/7', False) ],   # Ratio 8/7 Color
        [[4,1], rgb_off_high              if config.get('10/9') == "Off"   else rgb_off_low               ],   # Ratio 10/9 Off
        [[5,1], rgb_white_high            if config.get('10/9') == "White" else rgb_white_low             ],   # Ratio 10/9 White
        [[6,1], getRatioRGB('10/9', True) if config.get('10/9') == "Color" else getRatioRGB('10/9', False)],   # Ratio 10/9 Color
        [[4,0], rgb_off_high              if config.get('9/8')  == "Off"   else rgb_off_low               ],   # Ratio 9/8 Off
        [[5,0], rgb_white_high            if config.get('9/8')  == "White" else rgb_white_low             ],   # Ratio 9/8 White
        [[6,0], getRatioRGB('9/8', True)  if config.get('9/8')  == "Color" else getRatioRGB('9/8', False) ],   # Ratio 9/8 Color
    ])

def displaySettingsPads(lpx):
    rgb_low  = [0.2, 0.2, 0.2]
    rgb_high = [1.0, 1.0, 1.0]
    rgb_red  = [0.2, 0.0, 0.0]
    rgb_48   = [0.2, 0.1, 0.3]
    rgb_48h  = [0.8, 0.2, 1.0]
    pads.display_multi(lpx, [
        [[0,7], rgb_red],                                                   # Send to channel 01
        [[1,7], rgb_high if config.get('send_channel_02')  else rgb_low],   # Send to channel 02
        [[2,7], rgb_high if config.get('send_channel_03')  else rgb_low],   # Send to channel 03
        [[3,7], rgb_high if config.get('send_channel_04')  else rgb_low],   # Send to channel 04
        [[4,7], rgb_high if config.get('send_channel_05')  else rgb_low],   # Send to channel 05
        [[5,7], rgb_high if config.get('send_channel_06')  else rgb_low],   # Send to channel 06
        [[6,7], rgb_high if config.get('send_channel_07')  else rgb_low],   # Send to channel 07
        [[7,7], rgb_high if config.get('send_channel_08')  else rgb_low],   # Send to channel 08
        [[0,6], rgb_high if config.get('send_channel_09')  else rgb_low],   # Send to channel 09
        [[1,6], rgb_high if config.get('send_channel_10')  else rgb_low],   # Send to channel 10
        [[2,6], rgb_high if config.get('send_channel_11')  else rgb_low],   # Send to channel 11
        [[3,6], rgb_high if config.get('send_channel_12')  else rgb_low],   # Send to channel 12
        [[4,6], rgb_high if config.get('send_channel_13')  else rgb_low],   # Send to channel 13
        [[5,6], rgb_high if config.get('send_channel_14')  else rgb_low],   # Send to channel 14
        [[6,6], rgb_high if config.get('send_channel_15')  else rgb_low],   # Send to channel 15
        [[7,6], rgb_red],                                                   # Send to channel 16

        [[0,4], rgb_high if config.get('pitch_bend_range_semitones') == 12  else rgb_low],   # Pitch range 12
        [[1,4], rgb_high if config.get('pitch_bend_range_semitones') == 24  else rgb_low],   # Pitch range 24
        [[2,4], rgb_48h  if config.get('pitch_bend_range_semitones') == 48  else rgb_48 ],   # Pitch range 48
        [[3,4], rgb_high if config.get('pitch_bend_range_semitones') == 96  else rgb_low],   # Pitch range 96
        
        [[7,0], rgb_high if config.get('help')  else rgb_low],   # Help
        
    ])
