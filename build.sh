#!/bin/bash


addon_root=$(dirname $(readlink -e ${0}))


print_step(){
    ten="          "
    spaces="${ten}${ten}${ten}${ten}${ten}${ten}${ten}${ten}${ten}"
    message="      - ${@}"
    message="${message:0:70}${spaces:0:$((70 - ${#message}))}"
    echo -ne "${message}"
}
print_sub_step(){
    ten="          "
    spaces="${ten}${ten}${ten}${ten}${ten}${ten}${ten}${ten}${ten}"
    message="          - ${@}"
    message="${message:0:70}${spaces:0:$((70 - ${#message}))}"
    echo -ne "${message}"
}
mark_step(){
    RED="\e[31m"
    GREEN="\e[32m"
    ENDCOLOR="\e[0m"
    status_message=""
    [[ ${1} == 'failed' ]] && status_message="${RED}[FAILED]${ENDCOLOR}"
    [[ ${1} == 'success' ]] && status_message="${GREEN}[SUCCESS]${ENDCOLOR}"
    echo -e "${status_message}"
}

# Make the install directory for the python libs
print_step "Creating lib directory"
rm -rf "${addon_root}/resources/lib"
mkdir -p "${addon_root}/resources/lib"
[[ $? > 0 ]] && mark_step failed && exit 1
mark_step success

# Install package and dependencies to lib directory
print_step "Creating Python venv"
rm -rf "${addon_root}/venv"
python3 -m venv "${addon_root}/venv"
[[ $? > 0 ]] && mark_step failed && exit 1
mark_step success

print_step "Installing dependencies"
source "${addon_root}/venv/bin/activate"
python3 -m pip install --target="${addon_root}/resources/lib" -r requirements.txt &> ${addon_root}/build.log
[[ $? > 0 ]] && mark_step failed && exit 1
mark_step success

# Read installed version
unmanic_version_long=$(cat ${addon_root}/resources/lib/unmanic/version  | jq -r '.long')
unmanic_version_short=$(cat ${addon_root}/resources/lib/unmanic/version  | jq -r '.short')
unmanic_version_major=$(echo ${unmanic_version_short} | cut -d. -f1)
unmanic_version_minor=$(echo ${unmanic_version_short} | cut -d. -f2)
unmanic_version_patch=$(echo ${unmanic_version_short} | cut -d. -f3)

# Update the long version to include a suffix "KODI"

print_step "Setting 'KODI' suffix to Unmanic module version"
sed -i "s|${unmanic_version_long}|${unmanic_version_long}KODI|g" "${addon_root}/resources/lib/unmanic/version"
[[ $? > 0 ]] && mark_step failed && exit 1
mark_step success

# Dynamically generate the addon.xml based on the version number of unmanic

print_step "Setting add-on version based on Unmanic release"
cp -f "${addon_root}/addon.template.xml" "${addon_root}/addon.xml"
sed -i "s|{VERSION}|${unmanic_version_major}.${unmanic_version_minor}.${unmanic_version_patch}|g" "${addon_root}/addon.xml"
[[ $? > 0 ]] && mark_step failed && exit 1
mark_step success

# Remove everything except the Python source
remove_extensions=(
    "ans"
    "bz2"
    "db"
    "dll"
    "exe"
    "gz"
    "mo"
    "pyc"
    "pyo"
    "so"
    "xbt"
    "xpr"
)
print_step "Cleaning out unnecessary binary files:"
mark_step
for ext in "${remove_extensions[@]}"; do
    print_sub_step "Delete all '*.${ext}' files..."
    find "${addon_root}/resources/lib" -type f -iname "*.${ext}" -delete 
    [[ $? > 0 ]] && mark_step failed && exit 1
    mark_step success
done
print_step "Cleaning out Python cache directories"
find "${addon_root}/resources/lib" -type d -name "__pycache__" -exec rm -rf {} +
[[ $? > 0 ]] && mark_step failed && exit 1
mark_step success
print_step "Cleaning out Python 'dist-info' directories"
find "${addon_root}/resources/lib" -type d -name "*.dist-info" -exec rm -rf {} +
[[ $? > 0 ]] && mark_step failed && exit 1
mark_step success

# Remove Python bin
print_step "Removing 'bin' Python directory"
rm -rf "${addon_root}/resources/lib/bin"
[[ $? > 0 ]] && mark_step failed && exit 1
mark_step success

# Remove Python module installation tools
remove_directories=(
    "_distutils_hack"
    "bin"
    "pkg_resources"
    "setuptools"
    "tests"
    "wheel"
)
print_step "Removing unnecessary Python package directories:"
mark_step
for directory in "${remove_directories[@]}"; do
    print_sub_step "Delete 'resources/lib/${directory}' directory..."
    rm -rf "${addon_root}/resources/lib/${directory}"
    [[ $? > 0 ]] && mark_step failed && exit 1
    mark_step success
done

# Ensure all files are not executable
print_step "Ensure all resources are not executable"
find "${addon_root}/resources" -type f -exec chmod a-x {} +
[[ $? > 0 ]] && mark_step failed && exit 1
mark_step success

exit 0
