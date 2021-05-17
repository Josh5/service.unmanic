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

import os
import sys
import pprint
import shutil
import subprocess
import xbmc
import xbmcvfs
import xbmcaddon
from resources import kodi_log_pipe

__addon__ = xbmcaddon.Addon()
__path__ = __addon__.getAddonInfo('path')
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')
__language__ = __addon__.getLocalizedString
__profile__ = xbmcvfs.translatePath(__addon__.getAddonInfo('profile'))
__unmanic_module_path__ = xbmcaddon.Addon('script.module.unmanic').getAddonInfo('path')

# Modify path to include lib directory
sys.path.append(xbmcvfs.translatePath(os.path.join(__path__, 'resources', 'lib')))


class UnmanicServiceHandle(object):
    unmanic_process = None
    # unmanic_command = [sys.executable, os.path.join(__path__, 'resources', 'lib', 'unmanic', 'service.py')]
    unmanic_command = [sys.executable, os.path.join(__unmanic_module_path__, 'lib', 'unmanic', 'service.py')]
    unmanic_env = {}

    def __init__(self):
        pass

    def start(self):
        """
        Start the Unmanic subprocess

        :return:
        """
        self.configure()

        # TODO: First check if binary dependencies are installed
        #   if not, offer to download and install them to addon_data.
        #   Do not start unmanic service unless all dependencies are satisfied.
        #   Show notification and exit if missing dependencies
        if not shutil.which("ffmpeg"):
            # Unable to find FFMPEG in PATH
            xbmc.log("Unmanic failed to find ffmpeg in PATH", level=xbmc.LOGINFO)
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (__addonname__, __language__(31001), 5000, __icon__))
            return
        else:
            xbmc.log("Unmanic: Found FFMPEG in path - '{}'".format(shutil.which("ffmpeg")), level=xbmc.LOGDEBUG)

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
        if self.unmanic_process:
            self.unmanic_process.terminate()

    def poll(self):
        """
        Poll Unmanic subprocess running state

        :return:
        """
        return self.unmanic_process.poll()

    def configure(self):
        xbmc.log("Configure Unmanic environment", level=xbmc.LOGINFO)

        # Write settings to json file
        os.environ['HOME_DIR'] = os.path.join(__profile__)
        os.environ['CONFIG_PATH'] = os.path.join(__profile__, '.unmanic', 'config')

        # If the dependency bin path exists, append it to the ENV PATH
        if os.path.exists(os.path.join(__profile__, 'bin')):
            os.environ['PATH'] = ':'.join([os.getenv('PATH'), os.path.join(__profile__, 'bin')])

        # Also write settings to set in environment
        self.unmanic_env = os.environ.copy()
        self.unmanic_env['HOME_DIR'] = __profile__
        self.unmanic_env['UI_PORT'] = __addon__.getSetting("P_port")
        self.unmanic_env['CONFIG_PATH'] = os.path.join(__profile__, '.unmanic', 'config')
        self.unmanic_env['PYTHONPATH'] = os.path.join(__path__, 'resources', 'lib')
