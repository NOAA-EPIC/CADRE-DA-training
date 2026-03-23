#!/usr/bin/env bash

set -x

cdir=$(cd "$(dirname "$(readlink -f -n "${BASH_SOURCE[0]}" )" )" && pwd -P)
JEDI_PDIR="${cdir}/.."

module load git-lfs
cd "${JEDI_PDIR}"
git clone https://github.com/NOAA-EMC/GDASApp.git
cd GDASApp
# For specific hash
git checkout eba447f
git submodule update --init --recursive
# Run build script
./build.sh -f -a -d -t hercules
