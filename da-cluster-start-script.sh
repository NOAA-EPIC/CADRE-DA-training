#!/bin/bash
mkdir -p /opt/build 
mkdir -p /opt/dist
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

# install cmake
cd /opt/build 
curl -LO https://github.com/Kitware/CMake/releases/download/v3.23.1/cmake-3.23.1-linux-x86_64.sh && /bin/bash cmake-3.23.1-linux-x86_64.sh --prefix=/usr/local --skip-license
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
git clone -b release/1.6.0 --recurse-submodules https://github.com/jcsda/spack-stack.git
cd spack-stack
. ./setup.sh
spack compiler find
spack compiler rm gcc@12.3.0
spack install intel-oneapi-compilers
spack install intel-oneapi-mpi
spack compiler add `spack location -i intel-oneapi-compilers`/compiler/latest/linux/bin/intel64
spack external find wget
spack external find m4
spack external find git
spack external find curl
spack external find git-lfs
spack external find openssl
spack external find libjpeg-turbo
spack external find perl
spack external find python
spack external find cmake
spack external find diffutils 
spack install zlib
spack install cmake
spack install curl
spack install --add diffutils@3.8
spack module lmod refresh -y --delete-tree && source /usr/share/lmod/lmod/init/bash && module avail
echo "source /usr/share/lmod/lmod/init/bash" >> /root/.bashenv
echo "module use /opt/spack-stack/spack/share/spack/lmod/linux-ubuntu22.04-x86_64/Core" >> /root/.bashenv
echo "module load cmake intel-oneapi-compilers intel-oneapi-mpi " >> /root/.bashenv
echo "[[ -s ~/.bashenv ]] && source ~/.bashenv" >> /root/.bashrc
spack stack create env --site linux.default --template unified-dev --name unified-dev
tee /opt/spack-stack/envs/unified-dev/spack.yaml <<EOF
spack:
  concretizer:
    unify: when_possible

 
  view: false
  include:
  - site
  - common

  definitions:
  - compilers: ['%intel']
  - packages:
    - ufs-srw-app-env ^mapl@2.40.3 ^esmf@8.5.0
  specs:
  - matrix:
    - [\$packages]
    - [\$compilers]
    exclude:
        # jedi-tools doesn't build with Intel
    - jedi-tools-env%intel
EOF

cd /opt/spack-stack/envs/unified-dev
spack env activate -p .
cd /opt/spack-stack
. ./setup.sh 
spack concretize 2>&1 | tee log.concretize
spack install --verbose 2>&1 | tee log.install
tee /opt/spack-stack/envs/unified-dev/site/modules.yaml <<EOF1
modules:
  default:
    enable::
    - lmod
    tcl:
      include:
      # List of packages for which we need modules that are blacklisted by default
      - openmpi
      - mpich
      - python
EOF1

tee /root/.spack/linux/compilers.yaml <<EOF2
compilers:
- compiler:
    spec: gcc@=11.4.0
    paths:
      cc: /bin/gcc
      cxx: /bin/g++
      f77: /bin/gfortran
      fc: /bin/gfortran
    flags: {}
    operating_system: ubuntu22.04
    target: x86_64
    modules: []
    environment: {}
    extra_rpaths: []
- compiler:
    spec: intel@=2021.10.0
    paths:
      cc: /opt/spack-stack/spack/opt/spack/linux-ubuntu22.04-sapphirerapids/gcc-11.4.0/intel-oneapi-compilers-2023.2.1-3xn2ybliqcwcftqzx27l2ig5ufm24f26/compiler/latest/linux/bin/intel64/icc
      cxx: /opt/spack-stack/spack/opt/spack/linux-ubuntu22.04-sapphirerapids/gcc-11.4.0/intel-oneapi-compilers-2023.2.1-3xn2ybliqcwcftqzx27l2ig5ufm24f26/compiler/latest/linux/bin/intel64/icpc
      f77: /opt/spack-stack/spack/opt/spack/linux-ubuntu22.04-sapphirerapids/gcc-11.4.0/intel-oneapi-compilers-2023.2.1-3xn2ybliqcwcftqzx27l2ig5ufm24f26/compiler/latest/linux/bin/intel64/ifort
      fc: /opt/spack-stack/spack/opt/spack/linux-ubuntu22.04-sapphirerapids/gcc-11.4.0/intel-oneapi-compilers-2023.2.1-3xn2ybliqcwcftqzx27l2ig5ufm24f26/compiler/latest/linux/bin/intel64/ifort
    flags: {}
    operating_system: ubuntu22.04
    target: x86_64
    modules:
    - intel-oneapi-compilers
    environment: {}
    extra_rpaths: [] 
EOF2
cp /root/.spack/linux/compilers.yaml /opt/spack-stack/envs/unified-dev/site 
cd /opt/spack-stack
. ./setup.sh && source /usr/share/lmod/lmod/init/bash
cd /opt/spack-stack/envs/unified-dev
spack env activate -p .
spack module lmod refresh -y
spack stack setup-meta-modules
module use /opt/spack-stack/spack/share/spack/lmod/Core
module load stack-intel/2021.10.0
module load stack-openmpi

#Install Apptainer/Singularity
DEBIAN_FRONTEND=noninteractive apt install -y software-properties-common
DEBIAN_FRONTEND=noninteractive add-apt-repository -y ppa:apptainer/ppa 
DEBIAN_FRONTEND=noninteractive apt-get update -yq --allow-unauthenticated 
DEBIAN_FRONTEND=noninteractive apt install -y apptainer 
DEBIAN_FRONTEND=noninteractive apt install -y ruby-full
DEBIAN_FRONTEND=noninteractive apt install -y imagemagick

#Install Rocoto, LandDA container and required datasets.

su - ubuntu <<'EOF'

sudo gem install sqlite3
sudo gem install thread
sudo gem install pool

git clone https://github.com/christopherwharrop/rocoto.git
cd rocoto/
./INSTALL

cd /home/ubuntu

wget https://noaa-ufs-land-da-pds.s3.amazonaws.com/CADRE-2025/Land-DA_v2.1_inputs.tar.gz
wget https://noaa-ufs-land-da-pds.s3.amazonaws.com/CADRE-2025/ubuntu22.04-intel-landda-cadre25.img


tar -vxzf Land-DA_v2.1_inputs.tar.gz 

echo 'export PATH="$PATH:/home/ubuntu/rocoto/bin"' >> .bashrc

echo 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAoHZlCJT9Vc/FJDreza+Yl+q2ene0gYZTgfYs53/eUV' >> /home/ubuntu/.ssh/authorized_keys
chown ubuntu:ubuntu /home/ubuntu/.ssh/authorized_keys
chmod 600 /home/ubuntu/.ssh/authorized_keys

EOF
