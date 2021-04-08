#!/bin/bash


addon_root=$(dirname $(readlink -e ${0}))

# Make the install directory for the python libs
rm -rf "${addon_root}/resources/lib"
mkdir -p "${addon_root}/resources/lib"

# Install package and dependencies to lib directory
rm -rf "${addon_root}/venv"
python3 -m venv "${addon_root}/venv"
source "${addon_root}/venv/bin/activate"
python3 -m pip install --target="${addon_root}/resources/lib" -r requirements.txt

# Read installed version
unmanic_version_long=$(cat ${addon_root}/resources/lib/unmanic/version  | jq -r '.long')
unmanic_version_short=$(cat ${addon_root}/resources/lib/unmanic/version  | jq -r '.short')
unmanic_version_major=$(echo ${unmanic_version_short} | cut -d. -f1)
unmanic_version_minor=$(echo ${unmanic_version_short} | cut -d. -f2)
unmanic_version_patch=$(echo ${unmanic_version_short} | cut -d. -f3)

# Update the long version to include a suffix "KODI"
sed -i "s|${unmanic_version_long}|${unmanic_version_long}KODI|g" "${addon_root}/resources/lib/unmanic/version"

# Dynamically generate the addon.xml based on the version number of unmanic
cp -fv "${addon_root}/addon.template.xml" "${addon_root}/addon.xml"
sed -i "s|{VERSION}|${unmanic_version_major}.${unmanic_version_minor}.${unmanic_version_patch}|g" "${addon_root}/addon.xml"

# Remove everything except the Python source
find "${addon_root}/resources/lib" -type f -name "*.py[o|c]" -delete 
find "${addon_root}/resources/lib" -type d -name "__pycache__" -exec rm -rf {} +
find "${addon_root}/resources/lib" -type d -name "*.dist-info" -exec rm -rf {} +

# Remove redundant modules
rm -f "${addon_root}/resources/lib/uuid.py"

# Remove Python bin
rm -rf "${addon_root}/resources/lib/bin"

# Clean up Python VENV
rm -rf "${addon_root}/venv"
