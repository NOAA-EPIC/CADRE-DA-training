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

Download the Container
***********************

.. attention:: 

   The container is pre-staged for the CADRE DA training, so users at the training may skip this section.   

Users will first need to download the container if it is not already on their system. 
The container for the CADRE DA training is already available on the system used for the training. When trying to replicate the steps on another system, users will need to download it from the `Land DA Data Bucket <https://registry.opendata.aws/noaa-ufs-land-da/>`_ into the user's directory of choice. In the chosen directory, run: 

.. code-block:: console 
   
   wget https://noaa-ufs-land-da-pds.s3.amazonaws.com/CADRE-2025/ubuntu22.04-intel-landda-cadre25.img

This will download a container image named ``ubuntu22.04-intel-landda-cadre25.img``.

.. _SetUpContainer:

Set Up the Container
**********************

Create experiment variables that point to the location of the data (``${LANDDA_INPUTS}``) and the container image (``${img}``): 

.. code-block:: console

   export LANDDA_INPUTS=/home/ubuntu/inputs
   export img=/home/ubuntu/ubuntu22.04-intel-landda-cadre25.img

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
   * ``-i`` is the full path to the container image ( e.g., ``/home/ubuntu/ubuntu22.04-intel-landda-cadre25.img``).

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
   cp config_samples/samples_cadre/<cadre#_case_name>.yaml config.yaml

where ``<cadre#_case_name>.yaml`` is the name of one of the sample case files in the `samples_cadre <https://github.com/ufs-community/land-DA_workflow/tree/develop/parm/config_samples/samples_cadre>`_ directory. 

For example, when running the **cadre1** case, run:

.. code-block:: console

   cd parm
   cp config_samples/samples_cadre/cadre1_config.LND.era5.3dvar.ims.warmstart.yaml config.yaml

Modify variables in ``config.yaml`` as needed. For example, in **cadre1**, the Gulf Coast Blizzard hit the Gulf Coast late on January 20, 2025 and left land by January 23, 2025. To reduce the duration of the default forecast and save computational resources, users can change ``DATE_LAST_CYCLE`` to from January 25 to January 22 (``2025012200``):

.. code-block:: console 

   ACCOUNT: epic
   APP: LND
   ATMOS_FORC: era5
   COLDSTART: 'NO'
   COUPLER_CALENDAR: 2
   DATE_CYCLE_FREQ_HR: 24
   DATE_FIRST_CYCLE: 2025011900
   DATE_LAST_CYCLE: 2025012200
   ...

Users may configure other elements of an experiment in ``config.yaml`` if desired. For example, users may wish to choose a different ``EXP_CASE_NAME``or DA algorithm (via the ``JEDI_ALGORITHM`` variable). Users who wish to run a more complex experiment may change the values in ``config.yaml`` using information from Section :numref:`%s: Workflow Configuration Parameters <ConfigWorkflow>`. 

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
              model_ver: v2.1.0
                    IMO: 384
              FRAC_GRID: NO
         NPROCS_FCST_IC: 36
              OUTPUT_FH: 1 -1
       DATE_FIRST_CYCLE: 2025012000
   ...
          LND_CALC_SNET: .true.
                ACCOUNT: epic
               KEEPDATA: YES
   INFO::/home/ubuntu/land-DA_workflow/sorc/conda/envs/land_da/lib/python3.12/site-packages/uwtools/config/validator.py::L76::0 schema-validation errors found in Rocoto config
   INFO::/home/ubuntu/land-DA_workflow/sorc/conda/envs/land_da/lib/python3.12/site-packages/uwtools/rocoto.py::L66::0 Rocoto XML validation errors found

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

To run the experiment, users may submit tasks manually via ``rocotorun`` or use a script to automate submission.

.. _WflowOverviewC:

Workflow Overview
==================

.. include:: ../doc-snippets/wflow-task-table.rst

.. _automated-run:

Automated Run
==================

To submit jobs automatically, users should navigate to the experiment directory, download the ``run_expt.sh`` script, modify permissions, and run the script: 

.. code-block:: console

   cd /home/ubuntu/exp_case/<EXP_CASE_NAME>
   wget https://raw.githubusercontent.com/NOAA-EPIC/CADRE-DA-training/refs/heads/main/Day2/run_expt.sh .
   chmod 755 run_expt.sh
   ./run_expt.sh

where ``<EXP_CASE_NAME>`` is replaced with the actual name of the experiment directory (e.g., ``cadre1_lnd_era5_ims``).

To check the status of the experiment, see :numref:`Section %s <VerifySuccess>` on tracking experiment progress.

.. _manual-run-c:

Manual Submission
==================

To run the experiment manually, navigate to the experiment directory and issue a ``rocotorun`` command. For example: 

.. code-block:: console

   cd ../../exp_case/cadre1_lnd_era5_ims
   rocotorun -w land_analysis.xml -d land_analysis.db

Users will need to issue the ``rocotorun`` command multiple times. The tasks must be run in order, and ``rocotorun`` initiates the next task once its dependencies have completed successfully. 

See the :ref:`Workflow Overview <WflowOverviewC>` section to learn more about the steps in the workflow process.

.. _TrackProgressC:

Track Progress
================

To check on the job status, users on a system with a Slurm job scheduler may run: 

.. code-block:: console

   squeue -u $USER

To view the experiment status, run:

.. code-block:: console

   rocotostat -w land_analysis.xml -d land_analysis.db

If ``rocotorun`` was successful, the ``rocotostat`` command will print a status report to the console. For example:

.. code-block:: console

          CYCLE         TASK                        JOBID        STATE  EXIT STATUS   TRIES   DURATION
   ===================================================================================================
   202501190000          jcb                            1    SUCCEEDED            0       1       16.0
   202501190000    prep_data                            2    SUCCEEDED            0       1       42.0
   202501190000     pre_anal                            3    SUCCEEDED            0       1       17.0
   202501190000     analysis                            7    SUCCEEDED            0       1       80.0
   202501190000    post_anal                            8    SUCCEEDED            0       1        4.0
   202501190000     forecast   druby://10.29.93.209:38153   SUBMITTING            -       0          0
   202501190000   plot_stats                            -            -            -       -          -
   ===================================================================================================
   202501200000          jcb                            4    SUCCEEDED            0       1       16.0
   202501200000    prep_data                            -            -            -       -          -
   202501200000     pre_anal                            -            -            -       -          -
   202501200000     analysis                            -            -            -       -          -
   202501200000    post_anal                            -            -            -       -          -
   202501200000     forecast                            -            -            -       -          -
   202501200000   plot_stats                            -            -            -       -          -
   ===================================================================================================
   202501210000          jcb                            5    SUCCEEDED            0       1       16.0
   202501210000    prep_data                            -            -            -       -          -
   202501210000     pre_anal                            -            -            -       -          -
   202501210000     analysis                            -            -            -       -          -
   202501210000    post_anal                            -            -            -       -          -
   202501210000     forecast                            -            -            -       -          -
   202501210000   plot_stats                            -            -            -       -          -
   ===================================================================================================
   202501220000          jcb                            6    SUCCEEDED            0       1       16.0
   202501220000    prep_data                            -            -            -       -          -
   202501220000     pre_anal                            -            -            -       -          -
   202501220000     analysis                            -            -            -       -          -
   202501220000    post_anal                            -            -            -       -          -
   202501220000     forecast                            -            -            -       -          -
   202501220000   plot_stats                            -            -            -       -          -

Note that the status table printed by ``rocotostat`` only updates after each ``rocotorun`` command (whether issued manually or automatically). For each task, a log file is generated. These files are stored in ``/home/ubuntu/ptmp/test_*/com/output/logs``. 

The experiment has successfully completed when all tasks say SUCCEEDED under STATE. Other potential statuses are: QUEUED, SUBMITTING, RUNNING, DEAD, and UNAVAILABLE. Users may view the log files to determine why a task may have failed.


.. _check-output-c:

Check Experiment Output
=========================

.. include:: ../doc-snippets/check-output.rst

.. COMMENT: ref to LANDDAROOT in this snippet - factor out? reword?


.. _plotting-c:

Plotting Results
------------------

Additionally, in the ``plot`` subdirectory, users will find images depicting the results of the ``analysis`` task for each cycle as a scatter plot (``hofx_oma_YYYYMMDD_scatter.png``) and as a histogram (``hofx_oma_YYYYMMDD_histogram.png``). 

The scatter plot is named OBS-BKG (i.e., Observation Minus Background [OMB]), and it depicts a map of snow depth results. Blue points indicate locations where the observed values are less than the background values, and red points indicate locations where the observed values are greater than the background values. The title lists the mean and standard deviation of the absolute value of the OMB values. 

The histogram plots OMB values on the x-axis and frequency density values on the y-axis. The title of the histogram lists the mean and standard deviation of the real value of the OMB values. 

.. |logo1| image:: https://raw.githubusercontent.com/wiki/ufs-community/land-DA_workflow/images/LandDAScatterPlot.png
   :alt: Map of snow depth in millimeters (observation minus analysis)

.. |logo2| image:: https://raw.githubusercontent.com/wiki/ufs-community/land-DA_workflow/images/LandDAHistogram.png 
   :alt: Histogram of snow depth in millimeters (observation minus analysis) on the x-axis and frequency density on the y-axis

.. list-table:: Snow Depth Plots for 2000-01-04

   * - |logo1|
     - |logo2|

Downloading the Plots
^^^^^^^^^^^^^^^^^^^^^^^

.. note::

   There are many options for viewing plots, and instructions for this are highly machine dependent. Users should view the data transfer documentation for their system to secure copy files from a remote system (such as :term:`RDHPCS`) to their local system. The instructions provided here apply to the Land DA training platform and may not be relevant on other platforms. 

#. Open a new terminal window.
#. Type ``bash`` to ensure a bash shell.
#. Add your private key (e.g., ``ssh-add ~/.ssh/id_ed25519_student1``).
#. For each directory of plots, run: 

   .. code-block:: console

      rsync -v --rsh "ssh student#@137.75.93.46 ssh" ubuntu@controller:/home/ubuntu/exp_case/cadre1_lnd_era5_ims/com_dir/landda.202501##/plot/* plots/202501##

   In the command, replace:

   * ``student#`` with your actual student number,
   * ``landda.202501##`` with the cycle date, and
   * ``plots/202501##/`` with the correct cycle date.

This will create a ``plots`` directory and cycle subdirectory in your current working directory and download the plots.  

Appendix
**********

.. _build-exe:

Building the Executables
==========================

The executables come pre-built in the Land DA Container. However, users who are curious about building the executables using the ``app_build.sh`` script can follow the instructions here. 

#. Shell into the container.
   
   .. code-block:: console 
      
      singularity shell -B /home:/home /home/ubuntu/ubuntu22.04-intel-landda-cadre25.img

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

After building the executables, type ``exit`` and continue to :numref:`Section %s: Configure the Experiment <ConfigureExptC>`.

