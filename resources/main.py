#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    unmanic

    Written by:               Josh.5 <jsunnex@gmail.com>
    Date:                     06 Dec 2020, (16:17 AM)

    Copyright:
           Copyright (C) Josh Sunnex - All Rights Reserved

           Permission is hereby granted, free of charge, to any person obtaining a copy
           of this software and associated documentation files (the "Software"), to deal
           in the Software without restriction, including without limitation the rights
           to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
           copies of the Software, and to permit persons to whom the Software is
           furnished to do so, subject to the following conditions:

           The above copyright notice and this permission notice shall be included in all
           copies or substantial portions of the Software.

           THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
           EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
           MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
           IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
           DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
           OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
           OR OTHER DEALINGS IN THE SOFTWARE.

"""

import json
import os
import pprint
import xbmc
import xbmcvfs
import xbmcaddon
import subprocess
import threading
from resources import kodi_log_pipe
from unmanic.libs.singleton import SingletonType

__addon__ = xbmcaddon.Addon()
__path__ = __addon__.getAddonInfo('path')
__profile__ = xbmcvfs.translatePath(__addon__.getAddonInfo('profile'))


class UnmanicServiceHandle(object, metaclass=SingletonType):
    unmanic_process = None
    unmanic_command = ['python', os.path.join(__path__, 'resources', 'lib', 'unmanic', 'service.py')]
    unmanic_env = {}

    def __init__(self):
        pass

    def start(self):
        """
        Start the Unmanic subprocess

        :return:
        """
        self.configure()
        xbmc.log("Running Unmanic process", level=xbmc.LOGINFO)

        message = pprint.pformat(self.unmanic_env, indent=1)
        xbmc.log("Unmanic environment: \n%s" % (str(message)), level=xbmc.LOGDEBUG)
        xbmc.log("Unmanic command: \n%s" % (str(self.unmanic_command)), level=xbmc.LOGDEBUG)

        log_pipe = kodi_log_pipe.KodiLogPipe(xbmc.LOGINFO)
        self.unmanic_process = subprocess.Popen(self.unmanic_command, stdout=log_pipe, stderr=log_pipe,
                                                env=self.unmanic_env)

        # Return status of process
        return self.poll()

    def stop(self):
        """
        Stop the Unmanic subprocess

        :return:
        """
        xbmc.log("Terminating Unmanic process", level=xbmc.LOGINFO)
        self.unmanic_process.terminate()

    def poll(self):
        """
        Poll Unmanic subprocess running state

        :return:
        """
        return self.unmanic_process.poll()

    def configure(self):
        xbmc.log("Configure Unmanic environment", level=xbmc.LOGINFO)

        # Write settings to dump to settings json file
        settings_dict = {
            'CONFIG_PATH': os.path.join(__profile__, '.unmanic', 'config'),
            'LOG_PATH':    os.path.join(__profile__, '.unmanic', 'logs'),
            'DATABASE':    {
                "TYPE":           "SQLITE",
                "FILE":           os.path.join(__profile__, '.unmanic', 'config', 'unmanic.db'),
                "MIGRATIONS_DIR": os.path.join(__path__, 'resources', 'lib', 'unmanic', 'migrations'),
            },
            'UI_PORT':     xbmcaddon.Addon().getSetting('P_port'),
        }
        xbmc.log("Unmanic Settings.json: \n%s" % (str(pprint.pformat(settings_dict, indent=1))), level=xbmc.LOGDEBUG)

        # Write settings to json file
        settings_file = os.path.join(settings_dict['CONFIG_PATH'], 'settings.json')
        if not os.path.exists(settings_dict['CONFIG_PATH']):
            os.makedirs(settings_dict['CONFIG_PATH'])
        try:
            with open(settings_file, 'w') as outfile:
                json.dump(settings_dict, outfile, sort_keys=True, indent=4)
        except Exception as e:
            xbmc.log("Error writing Unmanic settings: {}".format(str(e)), level=xbmc.LOGERROR)

        # Also write settings to set in environment
        self.unmanic_env = os.environ.copy()
        self.unmanic_env['HOME_DIR'] = __profile__
        self.unmanic_env['CONFIG_PATH'] = settings_dict['CONFIG_PATH']
        self.unmanic_env['LOG_PATH'] = settings_dict['LOG_PATH']
