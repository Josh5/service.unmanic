#!/bin/bash
###
# File: release.sh
# Project: service.unmanic
# File Created: Thursday, 8th April 2021 8:26:57 pm
# Author: Josh.5 (jsunnex@gmail.com)
# -----
# Last Modified: Thursday, 8th April 2021 11:58:10 pm
# Modified By: Josh.5 (jsunnex@gmail.com)
###


project_directory=$(readlink -e $(dirname ${BASH_SOURCE[0]}))
tmp_dir=$(mktemp -d)


# Clone to temp directory
pushd ${project_directory} &> /dev/null

echo -e "\n*** Clone temp repo of project"
origin_url=$(git config --get remote.origin.url)
git clone --depth=1 "${origin_url}" "${tmp_dir}/service.unmanic"

popd  &> /dev/null


# Fetch git commit and if there are uncommitted chagnes
pushd ${project_directory} &> /dev/null

current_commit="$(git rev-parse --verify --short HEAD)"
dirty_repo="$(git diff-index --quiet HEAD -- || echo '(dirty)')"

popd  &> /dev/null


# Build addon
pushd ${tmp_dir}/service.unmanic &> /dev/null

echo -e "\n*** Checkout the 'release' branch in temp repo"
git checkout --orphan release

echo -e "\n*** Pull any previous changes in the 'release' branch in temp repo"
git pull origin release

echo -e "\n*** Installing updates to release branch in temp repo"
cp -rf ${project_directory}/* ${tmp_dir}/service.unmanic/
source ${tmp_dir}/service.unmanic/build.sh

echo -e "\n*** Modify gitignore for release branch in temp repo"
sed -i 's|/addon.xml.*|#|g' ${tmp_dir}/service.unmanic/.gitignore
sed -i 's|/resources/lib.*|#|g' ${tmp_dir}/service.unmanic/.gitignore

popd  &> /dev/null


# Cleanup release files
pushd ${tmp_dir}/service.unmanic &> /dev/null

rm -f  "${tmp_dir}/service.unmanic/addon.template.xml"
rm -f  "${tmp_dir}/service.unmanic/*.sh"
rm -f  "${tmp_dir}/service.unmanic/requirements.txt"

popd  &> /dev/null


# Commit changes
pushd ${tmp_dir}/service.unmanic &> /dev/null

echo -e "\n*** Commit changes in temp repo"
commit_message="Deploy add-on - based on ${current_commit} ${dirty_repo}"
git add .
git commit -m "${commit_message}"

popd  &> /dev/null


# Publish changes
pushd ${tmp_dir}/service.unmanic &> /dev/null

echo -e "\n*** Publish changes in temp repo"
git push origin release

popd  &> /dev/null
