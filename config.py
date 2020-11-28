import configparser
import os.path
from os import path

def get(k):
    if k == 'edo':
        return int(config['EDO']['edo'])
    elif k == 'root_note':
        return int(config['EDO']['root_note'])
    elif k == 'row_offset':
        return int(config['EDO']['row_offset'])
    elif k == 'edonote_offset':
        return int(config['EDO']['edonote_offset'])
    elif k == 'octave_offset':
        return int(config['EDO']['octave_offset'])
    elif k == 'help':
        return config['OTHER']['help'] == "True"
    elif k == 'launchpad_midi_id':
        return config['MIDI']['launchpad_midi_id']
    elif k == 'pitch_bend_range_semitones':
        return int(config['MPE']['pitch_bend_range_semitones'])
    elif k == 'send_channel_01':
        return config['MPE']['send_channel_01'] == "True"
    elif k == 'send_channel_02':
        return config['MPE']['send_channel_02'] == "True"
    elif k == 'send_channel_03':
        return config['MPE']['send_channel_03'] == "True"
    elif k == 'send_channel_04':
        return config['MPE']['send_channel_04'] == "True"
    elif k == 'send_channel_05':
        return config['MPE']['send_channel_05'] == "True"
    elif k == 'send_channel_06':
        return config['MPE']['send_channel_06'] == "True"
    elif k == 'send_channel_07':
        return config['MPE']['send_channel_07'] == "True"
    elif k == 'send_channel_08':
        return config['MPE']['send_channel_08'] == "True"
    elif k == 'send_channel_09':
        return config['MPE']['send_channel_09'] == "True"
    elif k == 'send_channel_10':
        return config['MPE']['send_channel_10'] == "True"
    elif k == 'send_channel_11':
        return config['MPE']['send_channel_11'] == "True"
    elif k == 'send_channel_12':
        return config['MPE']['send_channel_12'] == "True"
    elif k == 'send_channel_13':
        return config['MPE']['send_channel_13'] == "True"
    elif k == 'send_channel_14':
        return config['MPE']['send_channel_14'] == "True"
    elif k == 'send_channel_15':
        return config['MPE']['send_channel_15'] == "True"
    elif k == 'send_channel_16':
        return config['MPE']['send_channel_16'] == "True"
    elif k == '3/2':
        return config['RATIOS']['3/2']
    elif k == '4/3':
        return config['RATIOS']['4/3']
    elif k == '5/3':
        return config['RATIOS']['5/3']
    elif k == '5/4':
        return config['RATIOS']['5/4']
    elif k == '6/5':
        return config['RATIOS']['6/5']
    elif k == '7/4':
        return config['RATIOS']['7/4']
    elif k == '7/5':
        return config['RATIOS']['7/5']
    elif k == '7/6':
        return config['RATIOS']['7/6']
    elif k == '8/5':
        return config['RATIOS']['8/5']
    elif k == '8/7':
        return config['RATIOS']['8/7']
    elif k == '9/5':
        return config['RATIOS']['9/5']
    elif k == '9/7':
        return config['RATIOS']['9/7']
    elif k == '9/8':
        return config['RATIOS']['9/8']
    elif k == '10/7':
        return config['RATIOS']['10/7']
    elif k == '10/9':
        return config['RATIOS']['10/9']
    elif k == '12/7':
        return config['RATIOS']['12/7']

def set(k,v):
    if k == 'edo' and isinstance(v, int):
        config['EDO']['edo'] = str(v)
        writeConfig()
    elif k == 'root_note' and isinstance(v, int):
        config['EDO']['root_note'] = str(v)
        writeConfig()
    elif k == 'row_offset' and isinstance(v, int):
        config['EDO']['row_offset'] = str(v)
        writeConfig()
    elif k == 'edonote_offset' and isinstance(v, int):
        config['EDO']['edonote_offset'] = str(v)
        writeConfig()
    elif k == 'octave_offset' and isinstance(v, int):
        config['EDO']['octave_offset'] = str(v)
        writeConfig()
    elif k == 'help' and (v==True or v==False):
        config['OTHER']['help'] = "True" if v else "False"
        writeConfig()
    elif k == 'launchpad_midi_id' and isinstance(v, str):
        config['MIDI']['launchpad_midi_id'] = v
        writeConfig()
    elif k == 'pitch_bend_range_semitones' and isinstance(v, int):
        config['MPE']['pitch_bend_range_semitones'] = str(v)
        writeConfig()
    elif k == 'send_channel_01' and (v==True or v==False):
        config['MPE']['send_channel_01'] = "True" if v else "False"
        writeConfig()
    elif k == 'send_channel_02' and (v==True or v==False):
        config['MPE']['send_channel_02'] = "True" if v else "False"
        writeConfig()
    elif k == 'send_channel_03' and (v==True or v==False):
        config['MPE']['send_channel_03'] ="True" if v else "False"
        writeConfig()
    elif k == 'send_channel_04' and (v==True or v==False):
        config['MPE']['send_channel_04'] = "True" if v else "False"
        writeConfig()
    elif k == 'send_channel_05' and (v==True or v==False):
        config['MPE']['send_channel_05'] = "True" if v else "False"
        writeConfig()
    elif k == 'send_channel_06' and (v==True or v==False):
        config['MPE']['send_channel_06'] = "True" if v else "False"
        writeConfig()
    elif k == 'send_channel_07' and (v==True or v==False):
        config['MPE']['send_channel_07'] = "True" if v else "False"
        writeConfig()
    elif k == 'send_channel_08' and (v==True or v==False):
        config['MPE']['send_channel_08'] = "True" if v else "False"
        writeConfig()
    elif k == 'send_channel_09' and (v==True or v==False):
        config['MPE']['send_channel_09'] = "True" if v else "False"
        writeConfig()
    elif k == 'send_channel_10' and (v==True or v==False):
        config['MPE']['send_channel_10'] = "True" if v else "False"
        writeConfig()
    elif k == 'send_channel_11' and (v==True or v==False):
        config['MPE']['send_channel_11'] = "True" if v else "False"
        writeConfig()
    elif k == 'send_channel_12' and (v==True or v==False):
        config['MPE']['send_channel_12'] = "True" if v else "False"
        writeConfig()
    elif k == 'send_channel_13' and (v==True or v==False):
        config['MPE']['send_channel_13'] = "True" if v else "False"
        writeConfig()
    elif k == 'send_channel_14' and (v==True or v==False):
        config['MPE']['send_channel_14'] = "True" if v else "False"
        writeConfig()
    elif k == 'send_channel_15' and (v==True or v==False):
        config['MPE']['send_channel_15'] = "True" if v else "False"
        writeConfig()
    elif k == 'send_channel_16' and (v==True or v==False):
        config['MPE']['send_channel_16'] = "True" if v else "False"
        writeConfig()
    elif k == '3/2':
        config['RATIOS']['3/2'] = v
        writeConfig()
    elif k == '4/3':
        config['RATIOS']['4/3'] = v
        writeConfig()
    elif k == '5/3':
        config['RATIOS']['5/3'] = v
        writeConfig()
    elif k == '5/4':
        config['RATIOS']['5/4'] = v
        writeConfig()
    elif k == '6/5':
        config['RATIOS']['6/5'] = v
        writeConfig()
    elif k == '7/4':
        config['RATIOS']['7/4'] = v
        writeConfig()
    elif k == '7/5':
        config['RATIOS']['7/5'] = v
        writeConfig()
    elif k == '7/6':
        config['RATIOS']['7/6'] = v
        writeConfig()
    elif k == '8/5':
        config['RATIOS']['8/5'] = v
        writeConfig()
    elif k == '8/7':
        config['RATIOS']['8/7'] = v
        writeConfig()
    elif k == '9/5':
        config['RATIOS']['9/5'] = v
        writeConfig()
    elif k == '9/7':
        config['RATIOS']['9/7'] = v
        writeConfig()
    elif k == '9/8':
        config['RATIOS']['9/8'] = v
        writeConfig()
    elif k == '10/7':
        config['RATIOS']['10/7'] = v
        writeConfig()
    elif k == '10/9':
        config['RATIOS']['10/9'] = v
        writeConfig()
    elif k == '12/7':
        config['RATIOS']['12/7'] = v
        writeConfig()
        

def writeConfig():
    with open('conf.ini', 'w') as configfile:
        config.write(configfile)

# Init
config = configparser.ConfigParser()

if path.exists('conf.ini'):
    config.read('conf.ini')
else:
    config.read('conf_default.ini')
    writeConfig()
