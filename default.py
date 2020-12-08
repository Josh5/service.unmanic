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
import xbmcaddon
import sys

__addon__ = xbmcaddon.Addon()


class Default(object):

    def download_dependencies(self):
        from resources import fetch_dependencies
        dependencies = fetch_dependencies.UnmanicDependencies()
        dependencies.fetch_ffmpeg()

    def run(self):
        if len(sys.argv) > 1:
            exec_method = sys.argv[1]
            xbmc.log("Unmanic called with arg: '{}' - exists:{}".format(exec_method, hasattr(self, exec_method)),
                     level=xbmc.LOGDEBUG)
            getattr(self, exec_method)()
        else:
            __addon__.openSettings()


if __name__ == '__main__':
    default = Default()
    default.run()
