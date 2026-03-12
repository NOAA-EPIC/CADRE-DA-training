#!/bin/bash
mkdir -p /opt/build 
mkdir -p /opt/dist
mkdir -p /opt/modulefiles/intel-oneapi
mkdir -p /opt/modulefiles/intel-oneapi-mpi
mkdir -p /opt/modulefiles/rocoto

DEBIAN_FRONTEND=noninteractive apt-get update -yq --allow-unauthenticated 
DEBIAN_FRONTEND=noninteractive apt-get -yq upgrade
DEBIAN_FRONTEND=noninteractive apt install -y gcc g++ gfortran gdb
DEBIAN_FRONTEND=noninteractive apt install -y build-essential
DEBIAN_FRONTEND=noninteractive apt install -y libkrb5-dev
DEBIAN_FRONTEND=noninteractive apt install -y m4
DEBIAN_FRONTEND=noninteractive apt install -y git
DEBIAN_FRONTEND=noninteractive apt install -y git-lfs
DEBIAN_FRONTEND=noninteractive apt install -y bzip2
DEBIAN_FRONTEND=noninteractive apt install -y unzip
DEBIAN_FRONTEND=noninteractive apt install -y automake
DEBIAN_FRONTEND=noninteractive apt install -y autopoint
DEBIAN_FRONTEND=noninteractive apt install -y gettext
DEBIAN_FRONTEND=noninteractive apt install -y texlive
DEBIAN_FRONTEND=noninteractive apt install -y libcurl4-openssl-dev
DEBIAN_FRONTEND=noninteractive apt install -y libssl-dev
DEBIAN_FRONTEND=noninteractive apt install -y lua5.3
DEBIAN_FRONTEND=noninteractive apt install -y liblua5.3-dev
DEBIAN_FRONTEND=noninteractive apt install -y lua-posix

wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | gpg --dearmor | sudo tee /usr/share/keyrings/oneapi-archive-keyring.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" | sudo tee /etc/apt/sources.list.d/oneAPI.list
DEBIAN_FRONTEND=noninteractive apt update

DEBIAN_FRONTEND=noninteractive apt install -y --allow-downgrades intel-basekit=2024.2.1-98
DEBIAN_FRONTEND=noninteractive apt install -y --allow-downgrades intel-hpckit=2024.2.1-77
DEBIAN_FRONTEND=noninteractive apt install -y --allow-downgrades intel-oneapi-compiler-dpcpp-cpp=2024.2.1-1079

cd /opt/intel/oneapi/compiler
unlink latest
ln -s 2024.2 latest

#!/bin/bash

# install cmake
cd /opt/build
curl -LO https://github.com/Kitware/CMake/releases/download/v3.27.9/cmake-3.27.9-linux-x86_64.sh && /bin/bash cmake-3.27.9-linux-x86_64.sh --prefix=/usr/local --skip-license
# install lmod
wget https://sourceforge.net/projects/lmod/files/Lmod-8.7.tar.bz2
tar vxjf Lmod-8.7.tar.bz2
cd Lmod-8.7
./configure --prefix=/usr/share && make install
ln -s /usr/share/lmod/lmod/init/profile /etc/profile.d/z00_lmod.sh
echo "dash dash/sh boolean false" | debconf-set-selections
DEBIAN_FRONTEND=noninteractive dpkg-reconfigure dash
ls -l /bin/sh
DEBIAN_FRONTEND=noninteractive apt-get update -yq --allow-unauthenticated
#rm /etc/profile.d/modules.sh
#dpkg -S /etc/profile.d/modules.sh


cd /opt
git clone -b release/1.9.0 --recurse-submodules https://github.com/jcsda/spack-stack.git
cd spack-stack
. ./setup.sh

spack compiler find
spack compiler rm gcc@12.3.0

cd /root/.spack
mv packages.yaml packages.yaml.bak
tee /root/.spack/packages.yaml <<EOF
packages:
  gcc:
    externals:
    - spec: gcc@11.4.0 languages='c,c++,fortran'
      prefix: /usr
      extra_attributes:
        compilers:
          c: /usr/bin/gcc
          cxx: /usr/bin/g++
          fortran: /usr/bin/gfortran
EOF

export ONEAPIPATH='/opt/intel/oneapi'
export ONEAPIMPIPATH='/opt/intel'

tee /opt/spack-stack/configs/sites/tier2/linux.default/compilers.yaml <<EOF
compilers:
- compiler:
    spec: oneapi@2024.2.1
    paths:
      cc: ${ONEAPIPATH}/compiler/latest/bin/icx
      cxx: ${ONEAPIPATH}/compiler/latest/bin/icpx
      f77: ${ONEAPIPATH}/compiler/latest/bin/ifort
      fc: ${ONEAPIPATH}/compiler/latest/bin/ifort
    flags: {}
    operating_system: ubuntu22.04
    target: x86_64
    modules:
    - intel-oneapi/2024.2.1
    environment:
      prepend_path:
        MODULEPATH: '/opt/modulefiles'
    extra_rpaths: []
      #modules:
      #- spack-managed-x86-64_v3
      #- intel-oneapi-compilers/2024.2.1
      #    environment:
      #      set:
      #        # https://github.com/ufs-community/ufs-weather-model/issues/2015#issuecomment-1864438186
      #        I_MPI_EXTRA_FILESYSTEM: 'ON'
      #        # override system module settings for FC and F77 (they're set to ifx)
      #        F77: '/apps/spack-managed-x86_64_v3-v1.0/gcc-11.3.1/intel-oneapi-compilers-2024.2.1-podbez65l57ms4uba527kg7pomxk5y3m/compiler/2024.2/bin/ifort'
      #        FC: '/apps/spack-managed-x86_64_v3-v1.0/gcc-11.3.1/intel-oneapi-compilers-2024.2.1-podbez65l57ms4uba527kg7pomxk5y3m/compiler/2024.2/bin/ifort'
      #      prepend_path:
      #        PATH: /usr/bin
      #        LD_LIBRARY_PATH: /usr/lib:/usr/lib64
      #        CPATH: '/usr/include/c++/11:/usr/include/c++/11/x86_64-redhat-linux'
      #    extra_rpaths: []

EOF

tee /opt/spack-stack/configs/sites/tier2/linux.default/modules.yaml <<EOF
modules:
  default:
    enable::
    - lmod
    lmod:
      include:
      # List of packages for which we need modules that are blacklisted by default
      - python
      - openssl
EOF

tee /opt/spack-stack/configs/sites/tier2/linux.default/packages.yaml <<EOF
packages:
  # For addressing https://github.com/JCSDA/spack-stack/issues/1355
  #   Use system zlib instead of spack-built zlib-ng
  autoconf:
    externals:
    - spec: autoconf@2.71
      prefix: /usr
  automake:
    externals:
    - spec: automake@1.16.5
      prefix: /usr
# Don't use issues with openssl
#curl:
#  externals:
#  - spec: curl@7.76.1+gssapi+ldap+nghttp2
#    prefix: /usr
  gawk:
    externals:
    - spec: gawk@5.1.0
      prefix: /usr
  gettext:
    externals:
    - spec: gettext@0.21
      prefix: /usr
  git:
    externals:
    - spec: git@2.34.1
      prefix: /usr
  git-lfs:
    externals:
    - spec: git-lfs@3.0.2
      prefix: /usr
  gmake:
    externals:
    - spec: gmake@4.3
      prefix: /usr
  grep:
    externals:
    - spec: grep@3.7
      prefix: /usr
  groff:
    externals:
    - spec: groff@1.22.4
      prefix: /usr
# Don't use, incomplete installation!
#libtool:
#  externals:
#  - spec: libtool@2.4.6
#    prefix: /usr
  m4:
    externals:
    - spec: m4@1.4.18
      prefix: /usr
  openssl:
    externals:
    - spec: openssl@3.0.2
      prefix: /usr
  perl:
    externals:
    - spec: perl@5.34
      prefix: /usr
  sed:
    externals:
    - spec: sed@4.8
      prefix: /usr
#tar:
#  externals:
#  - spec: tar@1.34
#    prefix: /usr
  wget:
    externals:
    - spec: wget@1.21.2
      prefix: /usr
EOF

tee /opt/spack-stack/configs/sites/tier2/linux.default/packages_oneapi.yaml <<EOF
packages:
  all:
    compiler:: [oneapi@2024.2.1]
    providers:
      mpi:: [intel-oneapi-mpi@2021.13]
      # Remove the next three lines to switch to intel-oneapi-mkl
      blas:: [openblas]
      fftw-api:: [fftw]
      lapack:: [openblas]
  mpi:
    buildable: False
  intel-oneapi-mpi:
    buildable: False
    externals:
    - spec: intel-oneapi-mpi@2021.13
      modules:
      - intel-oneapi-mpi/2021.13
      environment:
      prepend_path:
        MODULEPATH: '/opt/modulefiles'
      prefix: ${ONEAPIMPIPATH}

  ectrans:
    require::
    - '@1.5.0 ~mkl +fftw'
  gsibec:
    require::
    - '@1.2.1 ~mkl'
  py-numpy:
    require::
    - '@1.26'
    - '^openblas'
  py-scipy:
    require:
      '%gcc'
EOF

tee /opt/modulefiles/intel-oneapi/2024.2.1.lua <<EOF
whatis([[Name : intel-oneapi-compilers]])
whatis([[Version : 2024.2.1]])
whatis([[Target : x86_64]])
whatis([[Short description : Intel oneAPI Compilers. Includes: icx, icpx, ifx, and ifort. Releases before 2024.0 include icc/icpc LICENSE INFORMATION: By downloading and using this software, you agree to the terms and conditions of the software license agreements at https://intel.ly/393CijO.]])

help([[Name   : intel-oneapi-compilers]])
help([[Version: 2024.2.1]])
help([[Target : x86_64]])
help()
help([[Intel oneAPI Compilers. Includes: icx, icpx, ifx, and ifort. Releases
before 2024.0 include icc/icpc LICENSE INFORMATION: By downloading and
using this software, you agree to the terms and conditions of the
software license agreements at https://intel.ly/393CijO.]])

family("compiler")

-- Loading this module unlocks the path below unconditionally
--prepend_path("MODULEPATH", "/apps/spack-2024-12/modules/linux-rocky9-x86_64/oneapi/2024.2.1")

prepend_path("MODULEPATH", "/opt/modulefiles")
prepend_path("CMAKE_PREFIX_PATH", "${ONEAPIPATH}/.", ":")
prepend_path("CMAKE_PREFIX_PATH", "${ONEAPIPATH}/compiler/2024.2", ":")
setenv("CMPLR_ROOT", "${ONEAPIPATH}/compiler/2024.2")
prepend_path("DIAGUTIL_PATH", "/apps/spack-2024-12/linux-rocky9-x86_64/gcc-11.4.1/intel-oneapi-compilers-2024.2.1-oqhstbmawnrsdw472p4pjsopj547o6xs/compiler/2024.2/etc/compiler/sys_check/sys_check.sh", ":")
prepend_path("DIAGUTIL_PATH", "${ONEAPIPATH}/compiler/2024.2/etc/compiler/sys_check/sys_check.sh", ":")
prepend_path("LD_LIBRARY_PATH", "/apps/spack-2024-12/linux-rocky9-x86_64/gcc-11.4.1/intel-oneapi-compilers-2024.2.1-oqhstbmawnrsdw472p4pjsopj547o6xs/compiler/2024.2/opt/compiler/lib:/apps/spack-2024-12/linux-rocky9-x86_64/gcc-11.4.1/intel-oneapi-compilers-2024.2.1-oqhstbmawnrsdw472p4pjsopj547o6xs/compiler/2024.2/lib", ":")
prepend_path("LD_LIBRARY_PATH", "${ONEAPIPATH}/compiler/2024.2/opt/compiler/lib:${ONEAPIPATH}/compiler/2024.2/lib", ":")
prepend_path("PKG_CONFIG_PATH", "${ONEAPIPATH}/compiler/2024.2/lib/pkgconfig", ":")
prepend_path("MANPATH", "${ONEAPIPATH}/compiler/2024.2/share/man:/usr/share/man", ":")
prepend_path("PATH", "${ONEAPIPATH}/compiler/2024.2/bin", ":")


setenv("F77", "${ONEAPIPATH}/compiler/latest/bin/ifort")
setenv("FC",  "${ONEAPIPATH}/compiler/latest/bin/ifort")
setenv("CC",  "${ONEAPIPATH}/compiler/latest/bin/icx")
setenv("CXX", "${ONEAPIPATH}/compiler/latest/bin/icpx")
setenv("SERIAL_F77", "${ONEAPIPATH}/compiler/latest/bin/ifort")
setenv("SERIAL_FC",  "${ONEAPIPATH}/compiler/latest/bin/ifort")
setenv("SERIAL_CC",  "${ONEAPIPATH}/compiler/latest/bin/icx")
setenv("SERIAL_CXX", "${ONEAPIPATH}/compiler/latest/bin/icpx")

setenv("INTEL_ONEAPI_COMPILERS_ROOT", "${ONEAPIPATH}")
append_path("MANPATH", "", ":")

EOF

tee /opt/modulefiles/intel-oneapi-mpi/2021.13.lua <<EOF
whatis("Name : intel-oneapi-mpi")
whatis("Version : 2021.13.1")
whatis("Target : x86_64")
whatis("Short description : Intel MPI Library is a multifabric message-passing library that implements the open-source MPICH specification. Use the library to create, maintain, and test advanced, complex applications that perform better on high-performance computing (HPC) clusters based on Intel processors.")
help([[Intel MPI Library is a multifabric message-passing library that
implements the open-source MPICH specification. Use the library to
create, maintain, and test advanced, complex applications that perform
better on high-performance computing (HPC) clusters based on Intel
processors. LICENSE INFORMATION: By downloading and using this software,
you agree to the terms and conditions of the software license agreements
at https://intel.ly/393CijO.]])

family("mpi")

prepend_path("MODULEPATH", "/opt/modulefiles")
prepend_path("CMAKE_PREFIX_PATH","${ONEAPIMPIPATH}/.")
prepend_path("CLASSPATH","${ONEAPIMPIPATH}/mpi/2021.13/share/java/mpi.jar")
prepend_path("CPATH","${ONEAPIMPIPATH}/mpi/2021.13/include")
prepend_path("FI_PROVIDER_PATH","${ONEAPIMPIPATH}/mpi/2021.13/opt/mpi/libfabric/lib:/usr/lib64/libfabric")
setenv("I_MPI_ROOT","${ONEAPIMPIPATH}/mpi/2021.13")
prepend_path("LD_LIBRARY_PATH","${ONEAPIMPIPATH}/mpi/2021.13/opt/mpi/libfabric/lib:${ONEAPIMPIPATH}/mpi/2021.13/lib")
prepend_path("LIBRARY_PATH","${ONEAPIMPIPATH}/mpi/2021.13/lib")
prepend_path("PKG_CONFIG_PATH","${ONEAPIMPIPATH}/mpi/2021.13/lib/pkgconfig")
prepend_path("MANPATH","${ONEAPIMPIPATH}/mpi/2021.13/share/man:/apps/slurm/default/share/man:/apps/lmod/lmod/share/man::/apps/local/man:/usr/share/man")
prepend_path("PATH","${ONEAPIMPIPATH}/mpi/2021.13/bin")
setenv("INTEL_ONEAPI_MPI_ROOT","${ONEAPIMPIPATH}")
append_path("MANPATH","")

EOF

tee /opt/modulefiles/rocoto/1.3.7.lua <<EOF
help([[
  Set environment variables for rocoto workflow manager)
]])

-- Make sure another version of the same package is not already loaded
conflict("rocoto")

-- Set environment variables
prepend_path("PATH","/home/ubuntu/rocoto/bin")
prepend_path("LD_LIBRARY_PATH","/home/ubuntu/rocoto/lib")

EOF

spack stack create env --site linux.default --template unified-dev --name ue-oneapi-2024.2.1 --compiler oneapi

tee /opt/spack-stack/envs/ue-oneapi-2024.2.1/spack.yaml <<EOF
# spack-stack hash: 261cfcc
# spack hash: f1be100187
spack:
  concretizer:
    unify: when_possible

  view: false
  include:
  - site
  - common

  definitions:
  - compilers:
    - '%oneapi'
  - packages:
     - global-workflow-env   ^esmf@=8.6.1 ^crtm@=3.1.1-build1 ^crtm-fix@=3.1.1.3
     - jedi-fv3-env
     - jedi-neptune-env      ^esmf@=8.8.0
     - jedi-tools-env
     - neptune-env           ^esmf@=8.8.0
     - neptune-python-env    ^esmf@=8.8.0
     - ufs-srw-app-env       ^esmf@=8.8.0 ^crtm@=3.1.1-build1 ^crtm-fix@=3.1.1.3
     - ufs-weather-model-env ^esmf@=8.8.0 ^crtm@=3.1.1-build1 ^crtm-fix@=3.1.1.3
     - crtm@2.4.0.1
     - mapl@2.53.4 ^esmf@8.8.0
     - esmf@=8.8.0 snapshot=none
  specs:
  - matrix:
    - [\$packages]
    - [\$compilers]
    exclude:
    # Don't build ai-env and jedi-tools-env with Intel or oneAPI,
    # some packages don't build (e.g., py-torch in ai-env doesn't
    # build with Intel, and there are constant problems concretizing
    # the environment
    - ai-env%intel
    - ai-env%oneapi
    - jedi-tools-env%intel
    - jedi-tools-env%oneapi
  - zlib@1.2.13
  - py-click@8.1.7
  packages:
    all:
      prefer: ['%oneapi']
      providers:
        mpi: [intel-oneapi-mpi]
EOF

cd /opt/spack-stack/envs/ue-oneapi-2024.2.1
spack env activate -p .
spack compiler find 
spack compiler rm gcc@12.3.0
spack compiler rm oneapi@2024.2.1
spack compiler add `spack location -i intel-oneapi-compilers` $ONEAPIPATH/compiler/latest/bin/
spack concretize 2>&1 | tee log.concretize
spack install --verbose --fail-fast --show-log-on-error --no-check-signature 2>&1 | tee log.install

spack module lmod refresh -y
spack stack setup-meta-modules

spack env deactivate

### Add Ruby
DEBIAN_FRONTEND=noninteractive apt-get update -yq --allow-unauthenticated
DEBIAN_FRONTEND=noninteractive apt install -y ruby-full

su - ubuntu <<'EOF'


sudo gem install sqlite3
sudo gem install thread
sudo gem install pool

git clone https://github.com/christopherwharrop/rocoto.git
cd rocoto/
./INSTALL

cd /home/ubuntu

echo 'export PATH="$PATH:/home/ubuntu/rocoto/bin"' >> .bashrc
echo 'module use /opt/modulefiles' >> .bashrc
echo 'module use /opt/spack-stack/envs/ue-oneapi-2024.2.1/install/modulefiles/Core' >> .bashrc
echo 'module use /opt/spack-stack/envs/ue-oneapi-2024.2.1/install/modulefiles/gcc' >> .bashrc
echo 'module use /opt/spack-stack/envs/ue-oneapi-2024.2.1/install/modulefiles/intel-oneapi-mpi/2021.13-dsdmcwn/gcc/11.4.0' >> .bashrc


EOF
