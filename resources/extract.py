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

import os
import xbmc
import zipfile
import tarfile


def extract_all(_in, _out, dp=None):
    # Ensure destination exists
    if not os.path.exists(_out):
        os.makedirs(_out)

    # Check file extension
    if _in.endswith('.zip'):
        xbmc.log('Unmanic: ZIP archive detected', level=xbmc.LOGDEBUG)
        if dp:
            return zip_with_progress(_in, _out, dp)
        return zip_no_progress(_in, _out)
    elif _in.endswith('.tar') or _in.endswith('.tar.xz') or _in.endswith('.tar.gz'):
        xbmc.log('Unmanic: TAR archive detected', level=xbmc.LOGDEBUG)
        return tar_with_progress(_in, _out, dp)
    else:
        xbmc.log('Unmanic: Unknown archive type - {}'.format(_in), level=xbmc.LOGERROR)
        return False


def zip_no_progress(_in, _out):
    try:
        archive = zipfile.ZipFile(_in, 'r')
        archive.extractall(_out)
    except Exception as e:
        xbmc.log('Unmanic: Error extracting file {} - {}'.format(_in, str(e)), level=xbmc.LOGERROR)
        return False
    return True


def zip_with_progress(_in, _out, dp):
    archive = zipfile.ZipFile(_in, 'r')
    number_of_files = float(len(archive.infolist()))
    count = 0
    try:
        for item in archive.infolist():
            count += 1
            update = (count / number_of_files * 100)
            dp.update(int(update))
            archive.extract(item, _out)
    except Exception as e:
        xbmc.log('Unmanic: Error while extracting file {} - {}'.format(_in, str(e)), level=xbmc.LOGERROR)
        return False
    return True


def tar_with_progress(_in, _out, dp):
    tar = None
    try:
        tar = tarfile.open(_in)
        open_tar = tar.getmembers()

        total = len(open_tar)
        dp.update(0)

        current_member = 0
        for member_info in open_tar:
            current_member += 1
            percent = int(current_member * 100.0 / total)

            dp.update(percent, '  -  {}'.format(member_info.name))

            if dp.iscanceled():
                tar.close()
                return False
            xbmc.log('Unmanic: Extracting file - {}'.format(member_info.name), level=xbmc.LOGDEBUG)
            try:
                tar.extractall(path=_out, members=[member_info])
                xbmc.log('Unmanic: File Extracted'.format(member_info.name), level=xbmc.LOGDEBUG)
            except Exception as e:
                xbmc.log('Unmanic: Exception while extracting file - {}'.format(member_info.name), level=xbmc.LOGERROR)

        tar.close()
        dp.update(100, ' ')
        return True
    except Exception as e:
        xbmc.log("Unmanic: Exception while extracting archive '{}' - {}".format(_in, str(e)), level=xbmc.LOGERROR)
        if tar:
            tar.close()
        return False
