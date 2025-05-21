.. _Container:

**********************************
Containerized Land DA Workflow
**********************************

These instructions will help users build and run a basic case for the Unified Forecast System (:term:`UFS`) Land Data Assimilation (DA) System using a `Singularity/Apptainer <https://apptainer.org/docs/user/latest/>`_ container. The Land DA :term:`container` packages together the Land DA System with its dependencies (e.g., :term:`spack-stack`, :term:`JEDI`) and provides a uniform environment in which to build and run the Land DA System. Normally, the details of building and running Earth system models will vary based on the computing platform because there are many possible combinations of operating systems, compilers, :term:`MPIs <MPI>`, and package versions available. Installation via Singularity/Apptainer container reduces this variability and allows for a smoother experience building and running Land DA. This approach is recommended for users not running Land DA on a supported :ref:`Level 1 <LevelsOfSupport>` system (e.g., Hera, Orion). 

This chapter provides instructions for building and running the Unified Forecast System (:term:`UFS`) Land DA System CADRE sample cases using a container. 

.. attention::

   This chapter of the User's Guide should **only** be used for container builds. For non-container builds, see :numref:`Chapter %s <BuildRunLandDA>`, which describes the steps for building and running Land DA on a :ref:`Level 1 System <LevelsOfSupport>` **without** a container. 

.. _Prereqs:

Prerequisites 
*****************

The containerized version of Land DA requires: 

   * `Installation of Apptainer <https://apptainer.org/docs/admin/latest/installation.html>`_ (or its predecessor, Singularity)
   * At least 26 CPU cores (may be possible to run with 13, but this has not been tested)
   * An **Intel** compiler and :term:`MPI` (available for `free here <https://www.intel.com/content/www/us/en/developer/tools/oneapi/hpc-toolkit-download.html>`_) 
   * The `Rocoto workflow manager <https://github.com/christopherwharrop/rocoto>`_
   * The `Slurm <https://slurm.schedmd.com/quickstart.html>`_ job scheduler

Apptainer is preinstalled for users at the CADRE DA training; users do **not** need to install it unless they are attempting to build and run the containerized Land DA System on a different platform. 

.. _GetDataC:

Data
***********

.. attention::

   Data is pre-staged for the CADRE DA training, and users at the training may skip this section. 

In order to run the Land DA System, users will need input data in the form of fix files, model forcing files, restart files, and observations for data assimilation. 

Data for the CADRE DA training are already available on the system used for the training. When attempting to replicate the steps on another system, users will need input data in the form of fix files, model forcing files, restart files, and observations for data assimilation. These files can be downloaded from the `Land DA Data Bucket <https://registry.opendata.aws/noaa-ufs-land-da/>`_ into the user's directory of choice. In the working directory, run: 

.. code-block:: console

   wget https://noaa-ufs-land-da-pds.s3.amazonaws.com/CADRE-2025/Land-DA_v2.1_inputs.tar.gz
   tar xvfz Land-DA_v2.1_inputs.tar.gz


.. _DownloadContainer:

Build the Container
**********************


.. COMMENT
   .. _ContainerBuild:

   Build the Container
   ======================

Download the Container
========================

.. attention:: 

   The container is pre-staged for the CADRE DA training, so users at the training may skip this section.   

Users will first need to download the container if it is not already on their system. 
The container for the CADRE DA training is already available on the system used for the training. When trying to replicate the steps on another system, users will need to download it from the `Land DA Data Bucket <https://registry.opendata.aws/noaa-ufs-land-da/>`_ into the user's directory of choice. In the chosen directory, run: 

.. code-block:: console 
   
   wget https://noaa-ufs-land-da-pds.s3.amazonaws.com/CADRE-2025/ubuntu22.04-intel-landda-daconsortium.img

This will download a container image named ``ubuntu22.04-intel-landda-daconsortium.img``.

.. _SetUpContainer:

Set Up the Container
**********************

Create experiment variables that point to the location of the data (``${LANDDA_INPUTS}``) and the container image (``${img}``): 

.. code-block:: console

   export LANDDA_INPUTS=/home/ubuntu/inputs
   export img=/home/ubuntu/ubuntu22.04-intel-landda-daconsortium.img

From your working directory, copy the ``setup_container.sh`` script out of the container. 

.. code-block:: console

   singularity exec -H $PWD $img cp -r /opt/land-DA_workflow/setup_container.sh .

The ``setup_container.sh`` script should now appear in your working directory. 

Run the ``setup_container.sh`` script with the proper arguments.

.. code-block:: console

   ./setup_container.sh -c=intelmpi/2021.13 -m=intelmpi/2021.13 -i=$img


where:

   * ``-c`` is the compiler on the user's local machine (e.g., ``intelmpi/2021.13``)

                  .. COMMENT previously intel/2022.1.2

   * ``-m`` is the :term:`MPI` on the user's local machine (e.g., ``intelmpi/2021.13``)
   * ``-i`` is the full path to the container image ( e.g., ``$LANDDAROOT/ubuntu22.04-intel-landda-release-public-v2.0.0.img``).

Running this script will print the following messages to the console:

.. code-block:: console

   Copying out land-DA_workflow from container
   Checking if LANDDA_INPUTS variable exists and linking to land-DA_workflow
   Land DA data exists, creating links
   Updating scripts files
   Updating singularity modulefiles
   Updating run related scripts
   Setup conda
   Getting the jedi test data from container
   Update experiment variables
   Creating links for exe
   Done

The user should now see the ``land-DA_workflow`` and ``jedi-bundle`` directories in their working directory. 

Containers come with pre-built executables, so users may continue to the next section to configure the experiment. However, users who are interested in learning how to build the executables can skip to :numref:`Section %s <build-exe>` to learn how to build their own executables to use in their experiment. 

.. _ConfigureExptC:

Configure the Experiment
**************************

To configure an experiment, first load the workflow modulefiles for the container: 

.. code-block:: console

   cd land-DA_workflow
   module use modulefiles
   module load wflow_singularity

Then navigate to the ``parm`` directory and copy the desired case into ``config.yaml``: 

.. code-block:: console

   cd parm
   cp config_samples/samples_cadre/cadre<case_name>.yaml config.yaml

where ``cadre<case_name>.yaml`` is the name of one of the sample case files in the `samples_cadre <https://github.com/ufs-community/land-DA_workflow/tree/develop/parm/config_samples/samples_cadre>`_ directory. 

For example, when running the **cadre2** case, run:

.. code-block:: console

   cd parm
   cp config_samples/samples_cadre/cadre2_config.LND.gswp3.letkf.ghcn.warmstart.yaml config.yaml

Generate the experiment directory by running:

.. code-block:: console

   ./setup_wflow_env.py -p=singularity

If the command runs without issue, this script will print override messages, experiment details, and "0 errors found" messages to the console, similar to the following excerpts: 

.. code-block:: console

   ubuntu@ip-10-29-93-226:~/land-DA_workflow/parm$ ./setup_wflow_env.py -p=singularity
    Python Log Level= str: INFO, attr: 20
   INFO::/home/ubuntu/land-DA_workflow/parm/./setup_wflow_env.py::L34:: Current directory (PARMdir): /home/ubuntu/land-DA_workflow/parm 
   INFO::/home/ubuntu/land-DA_workflow/parm/./setup_wflow_env.py::L36:: Home directory (HOMEdir): /home/ubuntu/land-DA_workflow 
   INFO::/home/ubuntu/land-DA_workflow/parm/./setup_wflow_env.py::L38:: Experimental base directory (exp_basedir): /home/ubuntu 
   INFO::/home/ubuntu/land-DA_workflow/parm/./setup_wflow_env.py::L168:: Experimental case directory /home/ubuntu/exp_case/cadre1_lnd_era5_ims has been created.
   INFO::/home/ubuntu/land-DA_workflow/parm/./setup_wflow_env.py::L175:: Rocoto YAML template: /home/ubuntu/land-DA_workflow/parm/templates/template.land_analysis.yaml
   **************************************************
   Overriding              ACCOUNT = epic
   Overriding                  APP = LND
   Overriding           ATMOS_FORC = era5
   ...
   Overriding        queue_default = batch
   Overriding               res_p1 = 97
   **************************************************
                   KEEPDATA: YES
                        RUN: landda
        nprocs_forecast_lnd: 36
          MED_COUPLING_MODE: ufs.nfrac.aoflux
              EXP_CASE_NAME: cadre1_lnd_era5_ims
                        NPZ: 127
   ...
                exp_basedir: /home/ubuntu
                        RES: 96
               ATM_LAYOUT_X: 3
             native_default: None
               ATM_LAYOUT_Y: 8
   DATM_STREAM_FN_LAST_DATE: 
               LND_LAYOUT_Y: 3
        LND_OUTPUT_FREQ_SEC: 21600
   INFO::/home/ubuntu/land-DA_workflow/sorc/conda/envs/land_da/lib/python3.12/site-packages/uwtools/config/validator.py::L76::0 schema-validation errors found in Rocoto config
   INFO::/home/ubuntu/land-DA_workflow/sorc/conda/envs/land_da/lib/python3.12/site-packages/uwtools/rocoto.py::L66::0 Rocoto XML validation errors found
   ubuntu@ip-10-29-93-226:~/land-DA_workflow/parm$ 

ATML Configurations Only
==========================

For :term:`ATML` configurations only (e.g., ``cadre3``), users must modify the ``run_container_executable.sh`` script using a code editor of their choice. For example: 

.. code-block:: console

   vim run_container_executable.sh

Uncomment the second-to-last line of the script, which adds the executables to the container by exporting the ``SINGULARITYENV_PREPEND_PATH`` variable:

.. code-block:: console

   # Uncomment the line below when running the ATML experiment
   export SINGULARITYENV_PREPEND_PATH=/home/ubuntu/land-DA_workflow/sorc/build/bin:$SINGULARITYENV_PREPEND_PATH
   ${SINGULARITYBIN} exec -B $BINDDIR:$BINDDIR -B $CONTAINERBASE:$CONTAINERBASE $INPUTBIND $img $cmd $arg

.. hint:: 

   When using ``vim``, hit the ``i`` key to enter insert mode and make any changes required. To close and save, hit the ``esc`` key and type ``:wq`` to write the changes to the file and exit/quit the file. Users may opt to use their preferred code editor instead. 

.. _RunExptC:

Run the Experiment
********************

To run the experiment, users can automate job submission via :term:`crontab` or submit tasks manually via ``rocotorun``. 

.. _WflowOverviewC:

Workflow Overview
==================

.. include:: ../doc-snippets/wflow-task-table.rst




To run the experiment, navigate to the experiment directory and issue a ``rocotorun`` command: 

.. code-block:: console

   cd ../../exp_case/cadre2_config.LND.gswp3.letkf.ghcn.warmstart
   rocotorun -w land_analysis.xml -d land_analysis.db

Users will need to issue the ``rocotorun`` command multiple times. The tasks must be run in order, and ``rocotorun`` initiates the next task once its dependencies have completed successfully. 

See the :ref:`Workflow Overview <wflow-overview>` section to learn more about the steps in the workflow process.

.. _TrackProgress:

Track Progress
================

To check on the job status, users on a system with a Slurm job scheduler may run: 

.. code-block:: console

   squeue -u $USER

To view the experiment status, run:

.. code-block:: console

   rocotostat -w land_analysis.xml -d land_analysis.db

See the :ref:`Track Experiment Status <VerifySuccess>` section to learn more about the ``rocotostat`` output.

.. _CheckExptOutput:

Check Experiment Output
=========================

Since this experiment in the container is the same experiment explained in the previous document section, it is suggested that users view the :ref:`experiment output structure <land-da-dir-structure>` and :ref:`plotting results <plotting>` sections to learn more about the expected experiment output. 

Appendix
**********

.. _build-exe:

Building the Executables
==========================

The executables come pre-built in the Land DA Container. However, users who are curious about building the executables using the ``app_build.sh`` script can follow the instructions here. 

#. Shell into the container.
   
   .. code-block:: console 
      
      singularity shell -B /home:/home /home/ubuntu/ubuntu22.04-intel-landda-daconsortium.img

#. Go to the ``land-DA_workflow`` directory in the container.

   .. code-block:: console

      cd /home/ubuntu/land-DA_workflow/sorc

#. Set up the environment by sourcing the container's spack-stack installation and loading the container modulefiles. 

   .. code-block:: console
      
      source /opt/spack-stack/spack-stack-1.6.0/envs/fms-2024.01/.bashenv-fms
      module use ../modulefiles
      module load build_singularity_intel

#. Build the model using ``app_build.sh``. Users must select either the :term:`ATML` configuration (``-a=ATML``) or the :term:`LND` configuration when building. Users indicate that the platform (``-p``) is a container using the ``-p=singularity`` argument. Conda was pre-built in previous steps, so users should include the ``--conda=off`` argument to avoid rebuilding it. The ``--build`` option keeps the executables in the ``build`` directory under ``bin``. 

   .. code-block:: console

      # Build ATML configuration (Noah-MP + FV3)
      ./app_build.sh -p=singularity -a=ATML --conda=off --build

      # Build LND configuration (Noah-MP + DATM)
      ./app_build.sh -p=singularity --conda=off --build


.. note:: 
   
   The ``parm/run_container_executable.sh`` script looks for the executables built by the ``app_build.sh`` script. If users decide not to use this script to build the ATML exectuables, then the ``run_container_executable.sh`` script will need to point to the location of the prebuilt executables: 

   * Pre-built LND executable: ``/opt/land-DA_workflow/install/bin``
   * Pre-built ATML executable: ``/opt/land-DA_workflow/sorc/build-atml/bin/``. 

After building the executables, continue to :numref:`Section %s: Configure the Experiment <ConfigureExptC>`.

