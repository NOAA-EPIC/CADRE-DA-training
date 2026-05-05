#!/usr/bin/env bash

set -x

cdir=$(cd "$(dirname "$(readlink -f -n "${BASH_SOURCE[0]}" )" )" && pwd -P)
JEDI_PDIR="${cdir}/.."

#module list
module purge
#module load git-lfs
#module list
cd "${JEDI_PDIR}"
git clone https://github.com/chan-hoo/GDASApp.git
cd GDASApp
# For specific hash
git checkout 441ffda
git submodule update --init --recursive
# Run build script
export BUILD_SOCA="OFF"
export BUILD_TESTING="OFF"
export GDASAPP_TESTDATA=""
./build.sh -f -a -t cluster > build.log 2>&1 &
date

