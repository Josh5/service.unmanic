#!/bin/bash


addon_root=$(dirname $(realpath ${0}))


# Make the install directory for the python libs
mkdir -p "${addon_root}/resources/lib"

# Install package and dependencies to lib directory
python3 -m pip  install --target="${addon_root}/resources/lib" unmanic