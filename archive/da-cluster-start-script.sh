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


### Add Ruby
DEBIAN_FRONTEND=noninteractive apt-get update -yq --allow-unauthenticated
DEBIAN_FRONTEND=noninteractive apt install -y ruby-full

### Install Apptainer
DEBIAN_FRONTEND=noninteractive apt install -y software-properties-common
DEBIAN_FRONTEND=noninteractive add-apt-repository -y ppa:apptainer/ppa
DEBIAN_FRONTEND=noninteractive apt-get update -yq --allow-unauthenticated
DEBIAN_FRONTEND=noninteractive apt install -y apptainer

su - ubuntu <<'EOF'


sudo gem install sqlite3
sudo gem install thread
sudo gem install pool

wget https://github.com/christopherwharrop/rocoto/archive/refs/tags/1.3.7.tar.gz
tar -vxzf 1.3.7.tar.gz
mv rocoto-1.3.7/ rocoto
cd rocoto/
./INSTALL

cd /home/ubuntu

echo 'export PATH="$PATH:/home/ubuntu/rocoto/bin"' >> .bashrc
echo 'module use /opt/modulefiles' >> .bashrc
echo 'module use /opt/spack-stack/envs/ue-oneapi-2024.2.1/install/modulefiles/Core' >> .bashrc
echo 'module use /opt/spack-stack/envs/ue-oneapi-2024.2.1/install/modulefiles/gcc/11.4.0' >> .bashrc
echo 'module use /opt/spack-stack/envs/ue-oneapi-2024.2.1/install/modulefiles/intel-oneapi-mpi/2021.13-*/gcc/11.4.0' >> .bashrc

cd /tmp/
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
sh Miniconda3-latest-Linux-x86_64.sh -b -p /home/ubuntu/miniconda3
/home/ubuntu/miniconda3/bin/conda init

### Download LandDA image

cd /home/ubuntu
mkdir LandDAtutorial 
cd LandDAtutorial
wget https://noaa-ufs-land-da-pds.s3.amazonaws.com/current_land_da_release_data/v3.0.0/ubuntu22.04-intel-landda-release-public-v3.0.0.img
wget https://noaa-ufs-land-da-pds.s3.amazonaws.com/current_land_da_release_data/v3.0.0/LandDAInputDatav3.0.0.tar.gz
tar -vxzf LandDAInputDatav3.0.0.tar.gz

EOF

