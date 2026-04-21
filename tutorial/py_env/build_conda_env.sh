module purge
module load miniconda3
conda env create -f environment.yml

# If you got:
# CondaError: Run 'conda init' before 'conda activate'
# Run the following commands

conda init bash
exec bash

conda activate plot_pyenv
conda list

#conda deactivate
