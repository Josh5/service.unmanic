#!/bin/bash
###
# File: release.sh
# Project: service.unmanic
# File Created: Thursday, 8th April 2021 8:26:57 pm
# Author: Josh.5 (jsunnex@gmail.com)
# -----
# Last Modified: Monday, 17th May 2021 10:11:31 pm
# Modified By: Josh.5 (jsunnex@gmail.com)
###


git_repo="git@github.com:Josh5/repo-scripts.git"
git_branch="matrix"


project_directory="$(readlink -e $(dirname $(readlink -e ${0}))/../)"
tmp_dir=$(mktemp -d --suffix='-unmanic-service-for-kodi')


# Fetch git commit and if there are uncommitted chagnes
pushd ${project_directory} &> /dev/null

current_commit="$(git rev-parse --verify --short HEAD)"
dirty_repo="$(git diff-index --quiet HEAD -- || echo '(dirty)')"

popd &> /dev/null


# Clone to temp directory
pushd ${project_directory} &> /dev/null

echo -e "\n*** Clone temp repo of project"
origin_url=$(git config --get remote.origin.url)
git clone --depth=1 --branch release --single-branch "${origin_url}" "${tmp_dir}/service.unmanic"

popd &> /dev/null


# Get the plugin version
plugin_version=$(python3 "${project_directory}/scripts/read_plugin_version.py" "${project_directory}")
unmanic_version=$(python3 "${project_directory}/scripts/read_unmanic_dependency_version.py" "${project_directory}")


# Build addon
pushd ${tmp_dir}/service.unmanic &> /dev/null

echo -e "\n*** Installing updates to release branch in temp repo"
rsync -ra --delete \
    --exclude='.git/' \
    --exclude='docs/' \
    --exclude='scripts/' \
    ${project_directory}/ ${tmp_dir}/service.unmanic/

echo -e "\n*** Modify gitignore for release branch in temp repo"

popd &> /dev/null


# Commit changes
pushd ${tmp_dir}/service.unmanic &> /dev/null

echo -e "\n*** Commit changes in temp repo"
commit_message="Deploy add-on - based on ${current_commit} ${dirty_repo} - Requires Unmanic v${unmanic_version}"
echo ${commit_message}
git add .
git commit -m "${commit_message}"
git tag -f ${unmanic_version}

popd &> /dev/null


# Publish changes
pushd ${tmp_dir}/service.unmanic &> /dev/null

echo -e "\n*** Publish changes in temp repo"
git push -f origin release --tags

popd &> /dev/null
