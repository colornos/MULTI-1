#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import logging
from configparser import ConfigParser
import os
import threading
import urllib3
import urllib.parse

http = urllib3.PoolManager()


class Plugin:

    def __init__(self):
        return

    def execute(self, config, temperaturedata):
        # self.temperaturedata = temperaturedata
        # --- part of plugin skeleton
        log = logging.getLogger(__name__)
        log.info('Starting plugin: ' + __name__)
        # read ini file from same location as plugin resides, named [pluginname].ini
        configfile = os.path.dirname(os.path.realpath(__file__)) + '/' + __name__ + '.ini'
        pluginconfig = ConfigParser()
        pluginconfig.read(configfile)
        log.info('ini read from: ' + configfile)
        # --- start plugin specifics here
        device = '104019001'
        f1 = open("rfid.txt", "r")
        if f1.mode == 'r':
            contents1 = f1.read()

        f2 = open("pin.txt", "r")
        if f2.mode == 'r':
            contents2 = f2.read()

        rfid = str(contents1)
        pin = str(contents2)

        if rfid == '0':
            print("No card detected!")

        else:
            temperature = temperaturedata[0]['temperature']
            headers = {
                'User-Agent': 'RaspberryPi/MBP70.py',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            form_data = {'rfid': rfid, 'pin': pin, 'one': temperature}
            encoded_data = urllib.parse.urlencode(form_data)
            r = http.request('POST', 'https://colornos.com/sensors/temperature.php', body=encoded_data, headers=headers)
            print(r.data)
            log.info('Finished plugin: ' + __name__)
