#!/bin/bash
###
# File: test.sh
# Project: service.unmanic
# File Created: Friday, 9th April 2021 1:21:58 pm
# Author: Josh.5 (jsunnex@gmail.com)
# -----
# Last Modified: Friday, 9th April 2021 1:26:48 pm
# Modified By: Josh.5 (jsunnex@gmail.com)
###


addon_root=$(dirname $(readlink -e ${0}))
test_path="$(readlink -e ~/.kodi/addons/service.unmanic)"


# Push addon to Kodi
pushd ${addon_root} &> /dev/null

if ! command -v inotifywait &> /dev/null; then
    echo "missing inotify-tools"
    exit 1
fi

while inotifywait --event modify --recursive ${addon_root} --exclude '.*~' &> /dev/null; do
    sleep 1
    echo -e "\n*** Pushing updates to Kodi add-ons directory"
    rsync -ra --delete \
        --exclude='.git/' \
        ${addon_root}/ ${test_path}/
    sleep 1
done

popd &> /dev/null
