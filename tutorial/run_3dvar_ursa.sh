#!/bin/bash -l
#SBATCH --account=epic
#SBATCH --job-name=fv3jedi
#SBATCH --output=log.cadre26.%j
#SBATCH --partition=u1-compute
#SBATCH --qos=batch
#SBATCH --time=00:10:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=96
#SBATCH --mem=128G
#SBATCH --exclusive

set -xue

ulimit -s unlimited; ulimit -a;

# Parameters
JEDI_BIN_PATH="/scratch4/NAGAPE/epic/Chan-hoo.Jeon/ufsda_test/jedi/build/bin"
JEDI_INPUT_PATH="/scratch4/NAGAPE/epic/Chan-hoo.Jeon/cadre26/input_data"
EXP_NAME_BASE="cadre26"

cdir=$(pwd)
exp_dir_path="${cdir}/exp_case/${EXP_NAME_BASE}.${SLURM_JOB_ID}"

# Set up experimental case directory
mkdir -p ${exp_dir_path}

# Copy input YAML files
cp -r ${cdir}/input_yaml/jedi_3dvar_fv3* ${exp_dir_path}

# Sym-link input directories
ln -nsf ${JEDI_INPUT_PATH}/* ${exp_dir_path}

# Copy diagnostic plotting scripts to experimental case directory
cp -r ${cdir}/diagnostics ${exp_dir_path}

# Move to experimental case directory
cd ${exp_dir_path}

# Create output directory
mkdir -p output

# Create plot_output directory
mkdir -p plot_output

# Load modules
module purge
module use /contrib/spack-stack/spack-stack-1.9.2/envs/ue-oneapi-2024.2.1/install/modulefiles/Core
module load stack-oneapi/2024.2.1
module load stack-intel-oneapi-mpi/2021.13
module load intel-oneapi-mkl/2024.2.1
module list

# Run FV3-JEDI
date
pgm="fv3jedi_var.x"
jedi_yaml="jedi_3dvar_fv3_2024022400.yaml"
srun -n 96 ${JEDI_BIN_PATH}/$pgm ${jedi_yaml} >>OUTPUT.fv3jedi 2>errfile_fv3jedi
export err=$?
if [[ $err != 0 ]]; then
  echo "FATAL ERROR: fv3-jedi failed."
  exit 1
fi
date
# Run JEDI executable for increment
pgm="gdas_fv3jedi_fv3inc.x"
jedi_inc_yaml="jedi_3dvar_fv3inc_2024022400.yaml"
srun -n 96 ${JEDI_BIN_PATH}/$pgm ${jedi_inc_yaml} >>OUTPUT.fv3inc 2>errfile_inc
export err=$?
if [[ $err != 0 ]]; then
  echo "FATAL ERROR: fv3-jedi increment failed."
  exit 1
fi
date
echo "===== FV3-JEDI completed successfully ====="
