#!/usr/bin/env bash

set -x

cdir=$(cd "$(dirname "$(readlink -f -n "${BASH_SOURCE[0]}" )" )" && pwd -P)
JEDI_PDIR="${cdir}/../jedi"
PLATFORM="hercules"
COMPILER="intel"

if [ -d "${JEDI_PDIR}" ]; then
  rm -rf ${JEDI_PDIR}
fi
mkdir -p ${JEDI_PDIR}
cd ${JEDI_PDIR}
git clone https://github.com/NOAA-EPIC/jedi-bundle.git
cd jedi-bundle

module purge
module load git-lfs
# For specific hash
git checkout 4802bc3
git submodule update --init --recursive
# Run build script
module use ${JEDI_PDIR}/jedi-bundle/modulefiles
module load ${PLATFORM}.${COMPILER}
module list
mkdir -p ${JEDI_PDIR}/build
cd ${JEDI_PDIR}/build
ecbuild "${JEDI_PDIR}/jedi-bundle" 2>&1 | tee log.jedibundle_ecbuild
make -j 4 2>&1 | tee log.jedibundle_make

