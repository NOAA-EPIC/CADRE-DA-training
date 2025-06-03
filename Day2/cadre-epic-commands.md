# Land DA System Training

## cadre1

`ssh student(#)@jump.epic.noaa.gov`

# Load environment modulefiles
cd land-DA_workflow
module use modulefiles
module load wflow_singularity

# Copy configuration 
cd parm
cp config_samples/samples_cadre/cadre1_config.LND.era5.3dvar.ims.warmstart.yaml config.yaml

# Edit config file
vim config.yaml
i
# Change DATE_LAST_CYCLE to 2025012200
# Save changes
:wq

# Set up experiment
./setup_wflow_env.py -p=singularity

# Navigate to experiment directory
cd ../../exp_case/cadre1_lnd_era5_ims/

# Run the experiment and check status repeatedly
rocotorun -w land_analysis.xml -d land_analysis.db
squeue -u $USER
rocotostat -w land_analysis.xml -d land_analysis.db

# OR
# Automate the workflow using the run_expt.sh script:
wget https://raw.githubusercontent.com/NOAA-EPIC/CADRE-DA-training/refs/heads/main/Day2/run_expt.sh /home/ubuntu/exp_case/cadre1_lnd_era5_ims
chmod 755 run_expt.sh
./run_expt.sh

# Navigate to the log directory
cd log_dir

# View the log file for any tasks that went DEAD
vim prep_data_2025012000.log

# Navigate to the plots directory (edit cycle date)
cd ../com_dir/landda.202501##/plot

# In new terminal window, type bash to ensure a bash shell and add your private key:
bash
ssh-add ~/.ssh/id_ed25519_student#

# Edit student number and cycle dates to download plots for each cycle:
rsync -v --rsh "ssh student#@jump.epic.noaa.gov ssh" ubuntu@controller:/home/ubuntu/exp_case/cadre1_lnd_era5_ims/com_dir/landda.202501##/plot/* ./plots/cadre1/202501##


## cadre2 

# Open a new terminal window and ssh to system:
ssh student(#)@jump.epic.noaa.gov

# Load the workflow environment:
cd land-DA_workflow
module use modulefiles
module load wflow_singularity

# Navigate to the parm directory to configure the new experiment:
cd parm

# Copy the new experiment configuration into config.yaml:
cp config_samples/samples_cadre/cadre2_config.LND.gswp3.letkf.ghcn.warmstart.yaml config.yaml

#Generate the experiment directory by running:
./setup_wflow_env.py -p=singularity

# Navigate to the experiment directory:
cd ../../exp_case/cadre2_lnd_gswp3_ghcn/

# Run the workflow launch command: 
rocotorun -w land_analysis.xml -d land_analysis.db

# To see jobs that are in progress: 
squeue -u $USER

# Check progress with rocotostat:
rocotostat -w land_analysis.xml -d land_analysis.db

# Automate the workflow using the run_expt.sh script:
wget https://raw.githubusercontent.com/NOAA-EPIC/CADRE-DA-training/refs/heads/main/Day2/run_expt.sh .
chmod 755 run_expt.sh
./run_expt.sh

## cadre3

# Shell into the container:
singularity shell -B /home:/home /home/ubuntu/ubuntu22.04-intel-landda-cadre25.img

# Go to the land-DA_workflow/sorc directory that was copied out of the container.
cd /home/ubuntu/land-DA_workflow/sorc

# Set up the environment
source /opt/spack-stack/spack-stack-1.6.0/envs/fms-2024.01/.bashenv-fms
module use ../modulefiles
module load build_singularity_intel

# Build the model using app_build.sh.
./app_build.sh -p=singularity -a=ATML --conda=off --build
exit

# Load the workflow environment:
cd land-DA_workflow
module use modulefiles
module load wflow_singularity

# Navigate to the parm directory to configure the new experiment:
cd /home/ubuntu/land-DA_workflow/parm

# Copy the new experiment configuration into config.yaml:
cp config_samples/samples_cadre/cadre3_config.ATML.3dvar.ghcn.coldstart.yaml config.yaml

# Generate the experiment directory by running:
./setup_wflow_env.py -p=singularity

# Modify run_container_executable.sh. For example:
vim run_container_executable.sh

# Uncomment the second-to-last line of the script:
export SINGULARITYENV_PREPEND_PATH=/home/ubuntu/land-DA_workflow/sorc/build/bin:$SINGULARITYENV_PREPEND_PATH

# Navigate to the experiment directory:
cd ../../exp_case/cadre3_atml/

# Run the workflow launch command: 
rocotorun -w land_analysis.xml -d land_analysis.db

# To see jobs that are in progress: 
squeue -u $USER

# Check progress with rocotostat:
rocotostat -w land_analysis.xml -d land_analysis.db

# Automate the workflow using the run_expt.sh script:
wget https://raw.githubusercontent.com/NOAA-EPIC/CADRE-DA-training/refs/heads/main/Day2/run_expt.sh .
chmod 755 run_expt.sh
./run_expt.sh

# Download plots
# Open a new terminal window.
bash

# Add your private key (e.g., ssh-add ~/.ssh/id_ed25519_student1).
# For each directory of plots, run: 
rsync -v --rsh "ssh student#@137.75.93.46 ssh" ubuntu@controller:/home/ubuntu/exp_case/cadre3_atml/com_dir/landda.20221222/plot/* plots/cadre3/20221222
# In the command above, replace student# with your actual student number




