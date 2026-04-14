#!/usr/bin/env bash

set -x

cdir=$(cd "$(dirname "$(readlink -f -n "${BASH_SOURCE[0]}" )" )" && pwd -P)
JEDI_PDIR="${cdir}/.."

module list
module purge
module load git-lfs
module list
cd "${JEDI_PDIR}"
git clone https://github.com/NOAA-EMC/GDASApp.git
cd GDASApp
# For specific hash
git checkout eba447f
git submodule update --init --recursive
# Run build script
export BUILD_SOCA="OFF"
./build.sh -f -a -d -t hercules > build.log 2>&1 &
