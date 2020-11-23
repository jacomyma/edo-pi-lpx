import configparser
import os.path
from os import path

def get(k):
    if k == 'edo':
        return config['EDO']['edo']
    elif k == 'root_note':
        return config['EDO']['root_note']
    elif k == 'row_offset':
        return config['EDO']['row_offset']
    elif k == 'launchpad_midi_id':
        return config['MIDI']['launchpad_midi_id']
    elif k == 'pitch_bend_range_semitones':
        return config['MPE']['pitch_bend_range_semitones']
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
    elif k == 'launchpad_midi_id' and isinstance(v, str):
        config['MIDI']['launchpad_midi_id'] = v
        writeConfig()
    elif k == 'pitch_bend_range_semitones' and isinstance(v, int):
        config['MPE']['pitch_bend_range_semitones'] = str(v)
        writeConfig()
    elif k == 'send_channel_01' and (v==True or v==False):
        config['MPE']['send_channel_01'] == "True" if v else "False"
        writeConfig()
    elif k == 'send_channel_01' and (v==True or v==False):
        config['MPE']['send_channel_01'] == "True" if v else "False"
        writeConfig()
    elif k == 'send_channel_01' and (v==True or v==False):
        config['MPE']['send_channel_01'] == "True" if v else "False"
        writeConfig()
    elif k == 'send_channel_02' and (v==True or v==False):
        config['MPE']['send_channel_02'] == "True" if v else "False"
        writeConfig()
    elif k == 'send_channel_03' and (v==True or v==False):
        config['MPE']['send_channel_03'] == "True" if v else "False"
        writeConfig()
    elif k == 'send_channel_04' and (v==True or v==False):
        config['MPE']['send_channel_04'] == "True" if v else "False"
        writeConfig()
    elif k == 'send_channel_05' and (v==True or v==False):
        config['MPE']['send_channel_05'] == "True" if v else "False"
        writeConfig()
    elif k == 'send_channel_06' and (v==True or v==False):
        config['MPE']['send_channel_06'] == "True" if v else "False"
        writeConfig()
    elif k == 'send_channel_07' and (v==True or v==False):
        config['MPE']['send_channel_07'] == "True" if v else "False"
        writeConfig()
    elif k == 'send_channel_08' and (v==True or v==False):
        config['MPE']['send_channel_08'] == "True" if v else "False"
        writeConfig()
    elif k == 'send_channel_09' and (v==True or v==False):
        config['MPE']['send_channel_09'] == "True" if v else "False"
        writeConfig()
    elif k == 'send_channel_10' and (v==True or v==False):
        config['MPE']['send_channel_10'] == "True" if v else "False"
        writeConfig()
    elif k == 'send_channel_11' and (v==True or v==False):
        config['MPE']['send_channel_11'] == "True" if v else "False"
        writeConfig()
    elif k == 'send_channel_12' and (v==True or v==False):
        config['MPE']['send_channel_12'] == "True" if v else "False"
        writeConfig()
    elif k == 'send_channel_13' and (v==True or v==False):
        config['MPE']['send_channel_13'] == "True" if v else "False"
        writeConfig()
    elif k == 'send_channel_14' and (v==True or v==False):
        config['MPE']['send_channel_14'] == "True" if v else "False"
        writeConfig()
    elif k == 'send_channel_15' and (v==True or v==False):
        config['MPE']['send_channel_15'] == "True" if v else "False"
        writeConfig()
    elif k == 'send_channel_16' and (v==True or v==False):
        config['MPE']['send_channel_16'] == "True" if v else "False"
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
