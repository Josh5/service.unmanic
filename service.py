#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    unmanic

    Written by:               Josh.5 <jsunnex@gmail.com>
    Date:                     06 Dec 2020, (7:21 AM)

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

import xbmc
import xbmcvfs
import xbmcaddon
import os
import sys
from resources import main

__addon__ = xbmcaddon.Addon()
__cwd__ = __addon__.getAddonInfo('path')
__scriptname__ = __addon__.getAddonInfo('name')
__version__ = __addon__.getAddonInfo('version')
__icon__ = __addon__.getAddonInfo('icon')
__ID__ = __addon__.getAddonInfo('id')
__language__ = __addon__.getLocalizedString
__profile__ = xbmcvfs.translatePath(__addon__.getAddonInfo('profile'))

sys.path.append(xbmcvfs.translatePath(os.path.join(__cwd__, 'resources', 'lib')))


class MyMonitor(xbmc.Monitor):
    def __init__(self, *args, **kwargs):
        xbmc.Monitor.__init__(self)
        self.unmanic_service_handle = main.UnmanicServiceHandle.__call__()

    def onSettingsChanged(self):
        # Fetch the unmanic service handle
        # Stop the process
        self.stop_unmanic()
        # Wait for process to terminate
        while not monitor.abortRequested():
            monitor.waitForAbort(2)
            if self.unmanic_service_handle.poll() is None:
                continue
            else:
                xbmc.log("Unmanic process stopped", level=xbmc.LOGINFO)
                break
        # Wait for a couple of seconds before restarting
        monitor.waitForAbort(2)
        # Start the Unmanic process
        self.start_unmanic()

    def start_unmanic(self):
        self.unmanic_service_handle.start()

    def stop_unmanic(self):
        self.unmanic_service_handle.stop()


if __name__ == '__main__':
    monitor = MyMonitor()

    monitor.start_unmanic()

    while not monitor.abortRequested():
        if monitor.waitForAbort(1):
            break

    monitor.stop_unmanic()
