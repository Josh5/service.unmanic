#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    unmanic

    Written by:               Josh.5 <jsunnex@gmail.com>
    Date:                     08 Dec 2020, (22:30 PM)

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
import xbmcgui
from urllib import request


def download(url, dest, dp=None):
    if not dp:
        dp = xbmcgui.DialogProgress()
        dp.create("Unmanic", "Downloading & Copying File", ' ', ' ')
    dp.update(0)
    request.urlretrieve(url, dest, lambda nb, bs, fs, url=url: _pbhook(nb, bs, fs, url, dp))


def _pbhook(numblocks, blocksize, filesize, url, dp):
    try:
        percent = int(min((numblocks * blocksize * 100) / filesize, 100))
        dp.update(percent)
    except Exception as e:
        xbmc.log('Unmanic: Completed file download - {}'.format(str(e)), level=xbmc.LOGDEBUG)
        percent = 100
        dp.update(percent)
    if dp.iscanceled():
        raise Exception("Canceled")
        dp.close()
