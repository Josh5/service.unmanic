#!/bin/bash


addon_root=$(dirname $(readlink -e ${0}))

# Make the install directory for the python libs
echo -e "\n      - Creating lib directory"
rm -rf "${addon_root}/resources/lib"
mkdir -p "${addon_root}/resources/lib"
[[ $? > 0 ]] && exit 1

# Install package and dependencies to lib directory
echo -e "\n      - Creating Python venv"
rm -rf "${addon_root}/venv"
python3 -m venv "${addon_root}/venv"
[[ $? > 0 ]] && exit 1

echo -e "\n      - Installing dependencies"
source "${addon_root}/venv/bin/activate"
python3 -m pip install --target="${addon_root}/resources/lib" -r requirements.txt
[[ $? > 0 ]] && exit 1

# Read installed version
unmanic_version_long=$(cat ${addon_root}/resources/lib/unmanic/version  | jq -r '.long')
unmanic_version_short=$(cat ${addon_root}/resources/lib/unmanic/version  | jq -r '.short')
unmanic_version_major=$(echo ${unmanic_version_short} | cut -d. -f1)
unmanic_version_minor=$(echo ${unmanic_version_short} | cut -d. -f2)
unmanic_version_patch=$(echo ${unmanic_version_short} | cut -d. -f3)

# Update the long version to include a suffix "KODI"
echo -e "\n      - Setting 'KODI' suffix to Unmanic module version"
sed -i "s|${unmanic_version_long}|${unmanic_version_long}KODI|g" "${addon_root}/resources/lib/unmanic/version"
[[ $? > 0 ]] && exit 1

# Dynamically generate the addon.xml based on the version number of unmanic
echo -e "\n      - Setting add-on version based on Unmanic release"
cp -f "${addon_root}/addon.template.xml" "${addon_root}/addon.xml"
sed -i "s|{VERSION}|${unmanic_version_major}.${unmanic_version_minor}.${unmanic_version_patch}|g" "${addon_root}/addon.xml"
[[ $? > 0 ]] && exit 1

# Remove everything except the Python source
echo -e "\n      - Cleaning out compiled Python files"
find "${addon_root}/resources/lib" -type f -name "*.py[o|c]" -delete 
[[ $? > 0 ]] && exit 1
echo -e "\n      - Cleaning out Python cache directories"
find "${addon_root}/resources/lib" -type d -name "__pycache__" -exec rm -rf {} +
[[ $? > 0 ]] && exit 1
echo -e "\n      - Cleaning out Python 'dist-info' directories"
find "${addon_root}/resources/lib" -type d -name "*.dist-info" -exec rm -rf {} +
[[ $? > 0 ]] && exit 1

# Remove redundant modules
echo -e "\n      - Removing 'uuid' Python module"
rm -f "${addon_root}/resources/lib/uuid.py"
[[ $? > 0 ]] && exit 1

# Remove Python bin
echo -e "\n      - Removing 'bin' Python directory"
rm -rf "${addon_root}/resources/lib/bin"
[[ $? > 0 ]] && exit 1

# Clean up Python VENV
echo -e "\n      - Cleaning up 'venv' directory"
rm -rf "${addon_root}/venv"
[[ $? > 0 ]] && exit 1

exit 0
