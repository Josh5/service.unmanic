#!/bin/bash
###
# File: test.sh
# Project: service.unmanic
# File Created: Friday, 9th April 2021 1:21:58 pm
# Author: Josh.5 (jsunnex@gmail.com)
# -----
# Last Modified: Monday, 17th May 2021 9:50:16 pm
# Modified By: Josh.5 (jsunnex@gmail.com)
###


project_directory="$(readlink -e $(dirname $(readlink -e ${0}))/../)"
test_path="$(readlink -e ~/.kodi/addons/service.unmanic)"


# Push addon to Kodi
pushd ${project_directory} &> /dev/null

if ! command -v inotifywait &> /dev/null; then
    echo "missing inotify-tools"
    exit 1
fi

while inotifywait --event modify --recursive ${project_directory} --exclude '.*~' &> /dev/null; do
    sleep 1
    echo -e "\n*** Pushing updates to Kodi add-ons directory"
    rsync -ra --delete \
        --exclude='.git/' \
        ${project_directory}/ ${test_path}/
    sleep 1
done

popd &> /dev/null
