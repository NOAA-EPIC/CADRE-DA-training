#!/bin/bash -l
##SBATCH --account=epic-explorer
##SBATCH --partition=hercules-2
##SBATCH --qos=cadre
#SBATCH --account=epic
#SBATCH --partition=hercules
#SBATCH --qos=batch
#SBATCH --job-name=fv3jedi
#SBATCH --output=log.cadre26.%j
#SBATCH --partition=hercules
#SBATCH --time=00:20:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=48
#SBATCH --mem=128G
###SBATCH --exclusive

set -xue

ulimit -s unlimited; ulimit -a;

# Parameters
# Path to JEDI bin direcoty: change this if you built this in another directory
JEDI_BIN_PATH="/work2/noaa/epic/weihuang/cadre/CADRE-DA-training/GDASApp/build/bin"

# Path to input files (pre-staged)
JEDI_INPUT_PATH="/work2/noaa/epic-explorer/cadre2026/input_data"

cdir=$(pwd)

# Prefix of experimental case directory
# Day 1 test:
#EXP_NAME_BASE="cadre26_Day1"
#yamldir="${cdir}/input_yaml/Day1"

# Day 2
#expname=exp_hyb_weight
#expname=exp_nicas_scale
#EXP_NAME_BASE="cadre26_Day2_${expname}"
#yamldir="${cdir}/input_yaml/Day2/${expname}"

# Day 3
#expname=exp_no_atms
#expname=exp_atms_err
 expname=exp_atm_thinning
 EXP_NAME_BASE="cadre26_Day3_${expname}"
 yamldir="${cdir}/input_yaml/Day3/${expname}"

# single_obs
#expname=ctrl
#expname=atms_err
#expname=hyb_weight
#expname=nicas_length_scale
#EXP_NAME_BASE="cadre26_single_obs_${expname}"
#yamldir="${cdir}/input_yaml/single_obs/${expname}"

exp_dir_path="${cdir}/exp_case/${EXP_NAME_BASE}.${SLURM_JOB_ID}"

# Set up experimental case directory
mkdir -p ${exp_dir_path}

# Copy input YAML files
#cp -r ${cdir}/input_yaml/jedi_3dvar_fv3* ${exp_dir_path}

# Sym-link input directories
ln -nsf ${JEDI_INPUT_PATH}/* ${exp_dir_path}

# Move to experimental case directory
cd ${exp_dir_path}

# Create output directory
mkdir -p output

# Load modules
module purge
module use /apps/contrib/spack-stack/spack-stack-1.9.2/envs/ue-oneapi-2024.1.0/install/modulefiles/Core
module load stack-oneapi/2024.2.1
module load stack-intel-oneapi-mpi/2021.13
module load intel-oneapi-mkl/2024.2.1
module load slurm
module list

# Run FV3-JEDI
date
pgm="fv3jedi_var.x"
jedi_yaml="${yamldir}/jedi_3dvar_fv3_2024022400.yaml"
srun -n 48 ${JEDI_BIN_PATH}/$pgm ${jedi_yaml} >>OUTPUT.fv3jedi 2>errfile_fv3jedi
export err=$?
if [[ $err != 0 ]]; then
  echo "FATAL ERROR: fv3-jedi failed."
  exit 1
fi
date
# Run JEDI executable for increment
pgm="gdas_fv3jedi_fv3inc.x"
jedi_inc_yaml="${yamldir}/jedi_3dvar_fv3inc_2024022400.yaml"
srun -n 48 ${JEDI_BIN_PATH}/$pgm ${jedi_inc_yaml} >>OUTPUT.fv3inc 2>errfile_inc
export err=$?
if [[ $err != 0 ]]; then
  echo "FATAL ERROR: fv3-jedi increment failed."
  exit 1
fi
date
echo "===== FV3-JEDI completed successfully ====="
