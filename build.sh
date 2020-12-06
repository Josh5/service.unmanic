#!/bin/bash


addon_root=$(dirname $(realpath ${0}))


# Make the install directory for the python libs
rm -rf "${addon_root}/resources/lib"
mkdir -p "${addon_root}/resources/lib"

# Install package and dependencies to lib directory
python3 -m pip install --upgrade --target="${addon_root}/resources/lib" unmanic

# Read installed version
unmanic_version_full=$(cat ${addon_root}/resources/lib/unmanic/version  | jq -r '.short')
unmanic_version_major=$(echo ${unmanic_version_full} | cut -d. -f1)
unmanic_version_minor=$(echo ${unmanic_version_full} | cut -d. -f2)
unmanic_version_patch=$(echo ${unmanic_version_full} | cut -d. -f3)

# Dynamically generate the addon.xml based on the version number of unmanic
cp -fv "${addon_root}/addon.template.xml" "${addon_root}/addon.xml"
sed -i "s|{VERSION}|${unmanic_version_major}.${unmanic_version_minor}.${unmanic_version_patch}|g" ${addon_root}/addon.xml

