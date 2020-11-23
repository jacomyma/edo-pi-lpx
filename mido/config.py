import configparser
import os.path
from os import path

def get(k):
    if k == 'edo':
        return config['EDO']['edo']

def set(k,v):
    if k == 'edo' and isinstance(v, int):
        config['EDO']['edo'] = str(v)
        writeConfig()

def writeConfig():
    with open('conf.ini', 'w') as configfile:
        config.write(configfile)

config = configparser.ConfigParser()

if path.exists('conf.ini'):
    config.read('conf.ini')
else:
    config.read('conf_default.ini')
    writeConfig()

set('edo',13)
print('Edo:', get('edo'))
