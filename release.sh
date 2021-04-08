#!/bin/bash
###
# File: release.sh
# Project: service.unmanic
# File Created: Thursday, 8th April 2021 8:26:57 pm
# Author: Josh.5 (jsunnex@gmail.com)
# -----
# Last Modified: Friday, 9th April 2021 2:10:07 am
# Modified By: Josh.5 (jsunnex@gmail.com)
###


project_directory=$(readlink -e $(dirname ${BASH_SOURCE[0]}))
tmp_dir=$(mktemp -d --suffix='-unmanic-service-for-kodi')


# Fetch git commit and if there are uncommitted chagnes
pushd ${project_directory} &> /dev/null

current_commit="$(git rev-parse --verify --short HEAD)"
dirty_repo="$(git diff-index --quiet HEAD -- || echo '(dirty)')"
unmanic_version="$(cat ./requirements.txt | cut -d= -f3)"

popd &> /dev/null


# Clone to temp directory
pushd ${project_directory} &> /dev/null

echo -e "\n*** Clone temp repo of project"
origin_url=$(git config --get remote.origin.url)
git clone --depth=1 --branch release --single-branch "${origin_url}" "${tmp_dir}/service.unmanic"

popd &> /dev/null


# Build addon
pushd ${tmp_dir}/service.unmanic &> /dev/null

echo -e "\n*** Installing updates to release branch in temp repo"
cp -rf ${project_directory}/* ${tmp_dir}/service.unmanic/

echo -e "\n*** Building add-on deps in temp repo"
chmod +x ./build.sh && ./build.sh
[[ $? > 0 ]] && echo "Build failed for some reason... Exit!" && exit 1

echo -e "\n*** Modify gitignore for release branch in temp repo"
sed -i 's|/addon.xml.*|#|g' ${tmp_dir}/service.unmanic/.gitignore
sed -i 's|/resources/lib.*|#|g' ${tmp_dir}/service.unmanic/.gitignore

popd &> /dev/null


# Cleanup release files
pushd ${tmp_dir}/service.unmanic &> /dev/null

echo -e "\n*** Remove template files for the release branch in temp repo"
rm -f  "${tmp_dir}/service.unmanic/addon.template.xml"
rm -f  "${tmp_dir}/service.unmanic/build.sh"
rm -f  "${tmp_dir}/service.unmanic/release.sh"
rm -f  "${tmp_dir}/service.unmanic/requirements.txt"

popd &> /dev/null


# Commit changes
pushd ${tmp_dir}/service.unmanic &> /dev/null

echo -e "\n*** Commit changes in temp repo"
commit_message="Deploy add-on - based on ${current_commit} ${dirty_repo} - Unmanic v${unmanic_version}"
git add .
git commit -m "${commit_message}"
git tag -f ${unmanic_version}

popd &> /dev/null


# Publish changes
pushd ${tmp_dir}/service.unmanic &> /dev/null

echo -e "\n*** Publish changes in temp repo"
git push -f origin release --tags

popd &> /dev/null
