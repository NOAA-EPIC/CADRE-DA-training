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

DEBIAN_FRONTEND=noninteractive apt install -y intel-basekit=2024.2.1-98
DEBIAN_FRONTEND=noninteractive apt install -y intel-hpckit=2024.2.1-77
DEBIAN_FRONTEND=noninteractive apt install -y intel-oneapi-compiler-dpcpp-cpp=2024.2.1-1079

cd /opt/intel/oneapi/compiler
unlink latest
ln -s 2024.2 latest
