#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    service.unmanic.contextitem.py

    Written by:               Josh.5 <jsunnex@gmail.com>
    Date:                     09 Apr 2021, (3:46 PM)

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

           THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
           EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
           MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
           IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
           DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
           OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
           OR OTHER DEALINGS IN THE SOFTWARE.

"""
import json
import os
import sys

import xbmc
import xbmcgui
import xbmcvfs
import xbmcaddon

__addon__ = xbmcaddon.Addon()
__path__ = __addon__.getAddonInfo('path')
__addonname__ = __addon__.getAddonInfo('name')
__version__ = __addon__.getAddonInfo('version')
__icon__ = __addon__.getAddonInfo('icon')
__ID__ = __addon__.getAddonInfo('id')
__language__ = __addon__.getLocalizedString
__profile__ = xbmcvfs.translatePath(__addon__.getAddonInfo('profile'))

from resources.lib import requests

files_for_unmanic = []


def post_new_pending_task(request_data):
    # Configure URL
    unmanic_port = __addon__.getSetting("P_port")
    unmanic_url = "http://{}:{}".format("localhost", unmanic_port)
    add_pending_tasks_url = "{}/api/v1/pending/add/".format(unmanic_url)

    # POST to Unmanic API
    r = requests.post(add_pending_tasks_url, json=request_data)

    # If the status code was not 200, then there is an issue with the API. Possibly unreachable?
    if not r.status_code != 200:
        show_error(__addon__.getLocalizedString(33004).format(unmanic_port))
        xbmc.log("Unable to reach Unmanic API", level=xbmc.LOGERROR)
        return {}
    return r.json()


def add_file_list_to_unmanic(file_list):
    for item in file_list:
        # Ensure the item is a file before sending it
        if not os.path.isfile(item):
            show_error(__addon__.getLocalizedString(33003).format(item))
            continue

        # Add item to request data and sent to Unmanic API
        request_data = {
            'path': item
        }
        xbmc.log("{} - Notifying Unmanic to add path to pending tasks list: {}".format(__addonname__, item),
                 level=xbmc.LOGDEBUG)
        result = post_new_pending_task(request_data)
        if not result.get('success'):
            xbmc.log("Unmanic did not add file: {}".format(item), level=xbmc.LOGERROR)


def execute_jsonrpc(request_data):
    response = xbmc.executeJSONRPC(json.dumps(request_data))
    j = json.loads(response)
    return j.get('result')


def get_file_info_from_jsonrpc(file_path):
    request = {
        'jsonrpc': '2.0',
        'method':  'Files.GetFileDetails',
        'params':  {
            'properties': [
                'title',
                'genre',
                'year',
                'rating',
                'runtime',
                'plot',
                'file',
                'art',
                'sorttitle',
                'originaltitle',
                'artist',
                'albumartist',
                'album',
                'duration',
                'trailer',
                'country',
                'season',
                'episode',
                'thumbnail',
                'tag',
                'albumlabel',
                'dateadded',
                'size'
            ],
            'file':       file_path,
            'media':      'files'
        },
        'id':      2
    }
    return execute_jsonrpc(request)


def split_list_item_path(list_item_path):
    path_split = list_item_path.split('?')
    for split in path_split:
        return split


def show_error(message):
    localized_error = __addon__.getLocalizedString(31017)
    xbmcgui.Dialog().notification(localized_error, message, xbmcgui.NOTIFICATION_ERROR, 10000)


def main():
    list_item_path = sys.listitem.getPath()
    xbmc.log("{} - Given list item path to send to Unmanic: {}".format(__addonname__, list_item_path),
             level=xbmc.LOGDEBUG)

    path_sans_params = split_list_item_path(list_item_path)
    path_info = get_file_info_from_jsonrpc(path_sans_params)

    if path_info is None:
        show_error(__addon__.getLocalizedString(33002).format(path_sans_params))
        return

    xbmc.log(json.dumps(path_info, indent=1), level=xbmc.LOGDEBUG)

    file_details = path_info.get("filedetails", {})
    if file_details and file_details.get('file'):
        add_file_list_to_unmanic([file_details.get('file')])


if __name__ == '__main__':
    main()
