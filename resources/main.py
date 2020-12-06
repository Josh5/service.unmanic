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
import xbmc
import xbmcvfs
import xbmcaddon
import subprocess
from unmanic.libs.singleton import SingletonType

unmanic_bin = xbmcvfs.translatePath(
    os.path.join(xbmcaddon.Addon().getAddonInfo('path'), 'resources', 'lib', 'bin', 'unmanic'))


class UnmanicServiceHandle(object, metaclass=SingletonType):
    unmanic_process = None
    unmanic_command = ['python', unmanic_bin]

    def __init__(self):
        pass

    def start(self):
        """
        Start the Unmanic subprocess

        :return:
        """
        xbmc.log("Running Unmanic process", level=xbmc.LOGINFO)
        self.unmanic_process = subprocess.Popen(self.unmanic_command, stdout=subprocess.PIPE)
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
        pass
