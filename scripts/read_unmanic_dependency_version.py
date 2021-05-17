#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: read_unmanic_dependency_version.py
# Project: Kodi-Module-Generator
# File Created: Friday, 17th May 2021 10:03:29 pm
# Author: Josh.5 (jsunnex@gmail.com)
# -----
# Last Modified: Monday, 17th May 2021 10:04:03 pm
# Modified By: Josh.5 (jsunnex@gmail.com)
###

import os
import sys
import xml.etree.ElementTree as ET

plugin_directory = " ".join(sys.argv[1:])

tree = ET.parse(os.path.join(plugin_directory, 'addon.xml'))
root = tree.getroot()

# Return version
version = "UNKNOWN"
for requires_element in root.findall("requires"):
    for import_element in requires_element.findall("import"):
        if import_element.attrib.get('addon') == 'script.module.unmanic':
            version = import_element.attrib.get('version')
            break

print(version)
