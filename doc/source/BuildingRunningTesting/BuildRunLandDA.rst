.. _BuildRunLandDA:

***********************************************
Land DA Workflow (Hera/Orion/Hercules/Gaea-C6)
***********************************************

This chapter provides instructions for building and running the Unified Forecast System (:term:`UFS`) Land DA System using a Jan. 19-20, 2025 00z sample :term:`LND` :term:`warmstart` case using :term:`ERA5` and :term:`IMS` data and the 3D-Var algorithm with the UFS Noah-MP land component and data atmosphere (:term:`DATM`) component.

.. attention::
   
   These steps are designed for use on :ref:`Level 1 <LevelsOfSupport>` systems (e.g., Hera, Orion) and may require significant changes on other systems. It is recommended that users on other systems run the containerized version of Land DA. Users may reference :numref:`Chapter %s: Containerized Land DA Workflow <Container>` for instructions.

.. COMMENT: Check that this is still the sampe case! And/or add others!

.. _create-dir:

Create a Working Directory
*****************************

Users can either create a new directory for their Land DA work (e.g., ``landda``) or choose an existing directory, depending on preference. Then, users should navigate to this directory. For example, to create a new directory and navigate to it, run: 

.. code-block:: console

   mkdir /path/to/landda
   cd /path/to/landda

where ``/path/to/landda`` is the path to the directory where the user plans to run Land DA experiments. In the experiment configuration file, this directory is referred to as ``$EXP_BASEDIR``. 

Optionally, users can save this directory path in an environment variable (e.g., ``$LANDDAROOT``) to avoid typing out full path names later. 

.. code-block:: console

   export LANDDAROOT=`pwd`

In this documentation, ``$LANDDAROOT`` is used, but users are welcome to choose another name for this variable if they prefer. 

.. _GetCode:

Get Code
***********

Clone the Land DA workflow repository. To clone the ``develop`` branch, run:

.. code-block:: console

   git clone -b develop --recursive https://github.com/ufs-community/land-DA_workflow.git

To clone the most recent release, run the same command with |branch| in place of ``develop``:

.. code-block:: console

   git clone -b release/public-v2.0.0 --recursive https://github.com/ufs-community/land-DA_workflow.git

.. _build-land-da:

Build the Land DA System
***************************

#. Navigate to the ``sorc`` directory.

   .. code-block:: console

      cd $LANDDAROOT/land-DA_workflow/sorc

#. Run the build script ``app_build.sh``:

   .. code-block:: console

      ./app_build.sh

   Users may need to press the ``Enter`` key to advance the build once the list of currently loaded modules appears. 
   If the code successfully compiles, the console output should include:
   
   .. code-block:: console

      [100%] Completed 'ufs_model.fd'
      [100%] Built target ufs_model.fd
      ...
      exit 0
   
   Additionally, the ``exec`` directory will contain the following executables: 

      * ``apply_incr.exe``
      * ``calcfIMS.exe``
      * ``tile2tile_converter.exe``
      * ``ufs_model``

.. _config-wflow:

Configure an Experiment
*************************

Several sample experiment configurations come with the Land DA System. Although this chapter outlines how to run the ``config.ATML.3dvar.ghcn.coldstart.yaml`` case, the following cases are available for use in the ``land-DA_workflow/parm/config_samples`` directory:

* ``config.ATML.3dvar.ghcn.coldstart.yaml``
* ``config.LND.era5.letkf.ghcn.coldstart.yaml``
* ``config.ATML.3dvar.ghcn.warmstart.yaml``
* ``config.LND.gswp3.3dvar.ghcn.coldstart.yaml``
* ``config.LND.era5.3dvar.ims.warmstart.yaml``
* ``config.LND.gswp3.letkf.ghcn.warmstart.yaml``

The sample configuration files are named based on their features: 

* Configuration (:term:`LND` or :term:`ATML`)
* Atmospheric forcing data (``gswp3`` or ``era5``) --- if any
* :term:`DA <DA>` algorithm (``letkf`` or ``3dvar``)
* Snow depth data (:term:`IMS` or :term:`GHCN`)
* Type of forecast start (i.e., :term:`warmstart` or :term:`coldstart`)

Users are encouraged to explore and modify the options available! 

.. _load-env:

Load the Workflow Environment
===============================

To load the workflow environment, run: 

.. include:: ../doc-snippets/load-env.rst

This activates the ``land_da`` conda environment, and the user typically sees ``(land_da)`` in front of the Terminal prompt at this point.

.. _configure-expt:

Modify the Workflow Configuration YAML
========================================

Copy the experiment settings into ``config.yaml``:

.. code-block:: console

   cd $LANDDAROOT/land-DA_workflow/parm
   cp config_samples/config.LND.era5.3dvar.ims.warmstart.yaml config.yaml

where ``<platform>`` is ``hera``, ``orion``, ``hercules``, or ``gaeac6``.
   
Users will need to configure the ``account`` variable in ``config.yaml`` and choose an ``EXP_CASE_NAME`` if a different name for the experiment is desired: 

   * ``account:`` A valid account name. Most NOAA :term:`RDHPCS` systems require a valid account name; other systems may not (in which case, any value will do).
   * ``EXP_CASE_NAME:`` This variable can be changed to any name the user wants (but note that whitespace and some punctuation characters are not allowed). However, the best names will indicate useful information about the experiment. This documentation uses ``lnd_era5_warmstart_00`` to indicate that it is an ERA5-LND warmstart case. 

.. note::

   To determine an appropriate ``account`` field for Level 1 systems that use the Slurm job scheduler, run ``saccount_params``. On other systems, running ``groups`` will return a list of projects that the user has permissions for. Not all listed projects/groups have an HPC allocation, but those that do are potentially valid account names. 

Users may configure other elements of an experiment in ``config.yaml`` if desired. For example, users may wish to alter ``DATE_FIRST_CYCLE``, ``DATE_LAST_CYCLE``, and/or ``DATE_CYCLE_FREQ_HR`` to indicate a different start cycle, end cycle, and increment. Users may also wish to change the DA algorithm from ``3dvar`` to ``letkf`` via the ``JEDI_ALGORITHM`` variable. Users who wish to run a more complex experiment may change the values in ``config.yaml`` using information from Sections :numref:`%s: Workflow Configuration Parameters <ConfigWorkflow>`, :numref:`%s: I/O for the Noah-MP Model <Model>`, and :numref:`%s: I/O for JEDI DA <DASystem>`. 

.. _GetData:

Data
------

:numref:`Table %s <Level1Data>` shows the locations of pre-staged data on NOAA :term:`RDHPCS` (e.g., Hera, Orion). These data locations are already linked to the Land DA System during the build but are provided here for informational purposes. 
   
.. _Level1Data:

.. list-table:: Level 1 RDHPCS Data
   :header-rows: 1

   * - Platform
     - Data Location
   * - Hera
     - /scratch2/NAGAPE/epic/UFS_Land-DA_|data|/inputs
   * - Hercules & Orion
     - /work/noaa/epic/UFS_Land-DA_|data|/inputs
   * - Gaea-C6
     - /gpfs/f6/bil-fire8/world-shared/UFS_Land-DA_|data|/inputs

Users who have difficulty accessing the data on Hera, Orion, Hercules, or Gaea-C6 may download it according to the instructions in :numref:`Section %s <GetDataC>`. Its subdirectories are soft-linked to the ``land-DA_workflow/fix`` directory by the build script (``sorc/app_build.sh``); when downloading new data, it should be placed in or linked to the ``fix`` directory.

.. _generate-wflow:

Set Up the Workflow
==============================

Generate the experiment directory by running: 

.. code-block:: console

   ./setup_wflow_env.py -p=<platform>

where ``<platform>`` is ``hera``, ``orion``, ``hercules``, or ``gaeac6``.

If the command runs without issue, override messages, experiment details, and "0 errors found" messages will be printed to the console, similar to the following excerpts: 

.. code-block:: console

   Python Log Level= str: INFO, attr: 20
   INFO::/path/to/setup_wflow_env.py::L34:: Current directory (PARMdir): /work/noaa/epic/username/hercules/landda/land-DA_workflow/parm 
   INFO::/path/to/setup_wflow_env.py::L36:: Home directory (HOMEdir): /work/noaa/epic/username/hercules/landda/land-DA_workflow 
   INFO::/path/to/setup_wflow_env.py::L38:: Experimental base directory (exp_basedir): /work/noaa/epic/username/hercules/landda 
   hercules
   INFO::/path/to/setup_wflow_env.py::L168:: Experimental case directory /work/noaa/epic/username/hercules/landda/exp_case/lnd_era5_warmstart_00 has been created.
   INFO::/path/to/setup_wflow_env.py::L175:: Rocoto YAML template: /work/noaa/epic/username/hercules/landda/land-DA_workflow/parm/templates/template.land_analysis.yaml
   **************************************************
   Overriding              ACCOUNT = epic
   Overriding                  APP = LND
   Overriding           ATMOS_FORC = era5
   ...
   Overriding    partition_default = hercules
   Overriding        queue_default = batch
   Overriding               res_p1 = 97
   **************************************************
               LND_LAYOUT_X: 1
   DATM_STREAM_FN_LAST_DATE: 
                JEDI_PY_VER: python3.10
   ...
                  model_ver: v2.1.0
                  OUTPUT_FH: 1 -1
                  DT_RUNSEQ: 3600
                   KEEPDATA: YES
   INFO::/path/to/uwtools/config/validator.py::L76::0 schema-validation errors found in Rocoto config
   INFO::/path/to/uwtools/rocoto.py::L66::0 Rocoto XML validation errors found

The setup script (``./setup_wflow_env.py``) will create an experiment directory, located by default at ``../../exp_case/${EXP_CASE_NAME}/``. It will populate this directory with the experiment configuration file (``land_analysis.yaml``), the workflow XML file (``land_analysis.xml``), and the workflow launch script (``launch_rocoto_wflow.sh``), as well as several directories described in :numref:`Table %s <expt_dir>` below. 

.. _expt_dir:

.. list-table:: Initial Experiment Directory
   :header-rows: 1

   * - File/Directory Name
     - Description
   * - ``com_dir``
     - Symlink to the ``ptmp/test_*/com/landda/v2.1.0`` directory, which contains output files for each cycle
   * - ``land_analysis.yaml``
     - Combines information from the user's ``config.yaml`` file with machine-specific values and calculated values that will be used in the experiment. 
   * - ``land_analysis.xml``
     - Workflow XML file used by the Rocoto workflow manager to determine which tasks (or "jobs") to submit to the batch system and when to submit them (e.g., when task dependencies are satisfied) 
   * - ``launch_rocoto_wflow.sh``
     - Workflow launch script
   * - ``log_dir``
     - Symlink to the directory containing log files for the Rocoto workflow (``ptmp/test_*/com/output/logs``)
   * - ``tmp_dir``
     - Symlink to the ``ptmp/test_*/tmp`` directory, which contains the working directory and temporary/intermediate files

.. COMMENT: Complete! 

Run the Experiment
********************

.. _wflow-overview:

Workflow Overview
==================

Each Land DA experiment includes multiple tasks that must be run in order to satisfy the dependencies of later tasks. These tasks are housed in the :term:`J-job <j-jobs>` scripts contained in the ``jobs`` directory. 

.. _WorkflowTasksTable:

.. list-table:: *J-job Tasks in the Land DA Workflow*
   :header-rows: 1

   * - J-job Task
     - Description
     - Application/Configuration
   * - JLANDDA_PREP_DATA
     - Prepares the observation / :term:`DATM` forcing data files
     - LND/ATML
   * - JLANDDA_FCST_IC 
     - Generates initial conditions (IC) files for the ATML configuration only
     - ATML
   * - JLANDDA_JCB
     - Generates JEDI configuration YAML file
     - LND/ATML
   * - JLANDDA_PRE_ANAL
     - Transfers the snow depth data from the restart files to the surface data files
     - LND
   * - JLANDDA_ANALYSIS
     - Runs :term:`JEDI` and adds the increment to the surface data files
     - LND/ATML
   * - JLANDDA_POST_ANAL
     - Transfers the JEDI snow depth result from the surface data files to the restart files
     - LND/ATML
   * - JLANDDA_FORECAST
     - Runs the forecast model
     - LND/ATML
   * - JLANDDA_PLOT_STATS
     - Plots the results of the ANALYSIS and FORECAST tasks
     - LND/ATML

Users may run these tasks :ref:`using the Rocoto workflow manager <run-w-rocoto>`. 

.. _run-w-rocoto:

Run With Rocoto
=================

To run the experiment, users can automate job submission via :term:`crontab` or submit tasks manually via ``rocotorun``. 

Automated Run
---------------

To automate task submission, users must be on a system where :term:`cron` is available. On Orion, cron is only available on the orion-login-1 node, and likewise on Hercules, it is only available on hercules-login-1, so users will need to work on those nodes when running cron jobs on Orion/Hercules.

On all platforms, users should navigate to the experiment directory and launch the workflow: 

.. code-block:: console

   cd ../../exp_case/lnd_era5_warmstart_00/
   ./launch_rocoto_wflow.sh add

To check the status of the experiment, see :numref:`Section %s <VerifySuccess>` on tracking experiment progress.

.. note::

   If users run into issues with the launch script, they can run ``conda deactivate`` before running the launch script. 

Manual Submission
-------------------

To run the experiment, issue a ``rocotorun`` command from the ``parm`` directory: 

.. code-block:: console

   rocotorun -w land_analysis.xml -d land_analysis.db

Users will need to issue the ``rocotorun`` command multiple times. The tasks must be run in order, and ``rocotorun`` initiates the next task once its dependencies have completed successfully. Details on checking experiment status are provided in the :ref:`next section <VerifySuccess>`.

.. _VerifySuccess:

Track Experiment Status
-------------------------

To view the experiment status, run: 

.. code-block:: console

   rocotostat -w land_analysis.xml -d land_analysis.db

If ``rocotorun`` was successful, the ``rocotostat`` command will print a status report to the console. For example:

.. code-block:: console

      CYCLE             TASK                        JOBID        STATE  EXIT STATUS   TRIES   DURATION
   =======================================================================================================
   202501190000          jcb                      5428846    SUCCEEDED            0       1        3.0
   202501190000    prep_data                      5428847    SUCCEEDED            0       1       30.0
   202501190000     pre_anal                      5428848    SUCCEEDED            0       1        8.0
   202501190000     analysis                      5428985    SUCCEEDED            0       1       72.0
   202501190000    post_anal                      5429034    SUCCEEDED            0       1        3.0
   202501190000     forecast                      5429128       QUEUED            -       0        0.0
   202501190000   plot_stats                            -            -            -       -          -
   =======================================================================================================
   202501200000          jcb                      5428849    SUCCEEDED            0       1       11.0
   202501200000    prep_data                      5428850    SUCCEEDED            0       1       30.0
   202501200000     pre_anal                      5428851    SUCCEEDED            0       1        3.0
   202501200000     analysis                      5428986    SUCCEEDED            0       1       71.0
   202501200000    post_anal                      5429035    SUCCEEDED            0       1        3.0
   202501200000     forecast  druby://130.18.14.151:46755   SUBMITTING            -       0        0.0
   202501200000   plot_stats                            -            -            -       -          -

Note that the status table printed by ``rocotostat`` only updates after each ``rocotorun`` command (whether issued manually or via cron automation). For each task, a log file is generated. These files are stored in ``$LANDDAROOT/ptmp/test/com/output/logs``. 

The experiment has successfully completed when all tasks say SUCCEEDED under STATE. Other potential statuses are: QUEUED, SUBMITTING, RUNNING, and DEAD. Users may view the log files to determine why a task may have failed.

.. _check-output:

Check Experiment Output
=========================

As the experiment progresses, it will generate a number of directories to hold intermediate and output files. The structure of those files and directories appears below:

.. _land-da-dir-structure:

.. code-block:: console

   $LANDDAROOT (<EXP_BASEDIR>): Base directory
    ├── land-DA_workflow (<HOMElandda> or <CYCLEDIR>): Home directory of the land DA workflow
    │     ├── jobs 
    │     ├── modulefiles
    │     ├── parm
    │     ├── scripts
    │     ├── sorc
    │     └── ush
    ├── exp_case
    │     ├── com_dir --> symlinked to ptmp/test_*/com/landda/v2.1.0
    │     ├── land_analysis.yaml
    │     ├── land_analysis.xml
    │     ├── launch_rocoto_wflow.sh
    │     ├── log_dir --> symlinked to ptmp/test_*/com/output/logs
    │     └── tmp_dir --> symlinked to ptmp/test_*/com/tmp
    └── ptmp (<PTMP>)
          └── test_* (<envir> or <OPSROOT>)
                └── com (<COMROOT>)
                │     ├── landda (<NET>)
                │     │     └── vX.Y.Z (<model_ver>)
                │     │           └── landda.YYYYMMDD (<RUN>.<PDY>): Directory containing the output files
                │     │                 ├── hofx
                │     │                 └── plot
                │     └── output
                │           └── logs (<LOGDIR>): Directory containing the log files for the Rocoto workflow
                └── tmp (<DATAROOT>)
                     ├── <jobid> (<DATA>): Working directory
                     └── DATA_SHARE
                           ├── YYYYMMDD (<PDY>): Directory containing the intermediate or temporary files
                           ├── hofx: Directory containing the soft links to the results of the analysis task for plotting
                           └── DATA_RESTART: Directory containing the soft links to the restart files for the next cycles

Each variable in parentheses and angle brackets (e.g., ``(<VAR>)``) is the name for the directory defined in the file ``land_analysis.yaml`` (derived from ``template.land_analysis.yaml`` or ``parm_xml.yaml``) or in the NCO Implementation Standards. For example, the ``<envir>`` variable is set to "test" (i.e., ``envir: "test"``) in ``template.land_analysis.yaml``. In the future, this directory structure will be further modified to meet the :nco:`NCO Implementation Standards<>`.

Check for the output files for each cycle in the experiment directory:

.. code-block:: console

   ls -l $LANDDAROOT/ptmp/test/com/landda/<model_ver>/landda.YYYYMMDD

where ``YYYYMMDD`` is the cycle date, and ``<model_ver>`` is the model version (currently |latestr| in the ``develop`` branch). The experiment should generate several restart files. 

.. _plotting:

Plotting Results
-----------------

Additionally, in the ``plot`` subdirectory, users will find images depicting the results of the ``analysis`` task for each cycle as a scatter plot (``hofx_oma_YYYYMMDD_scatter.png``) and as a histogram (``hofx_oma_YYYYMMDD_histogram.png``). 

The scatter plot is named OBS-ANA (i.e., Observation Minus Analysis [OMA]), and it depicts a map of snow depth results. Blue points indicate locations where the observed values are less than the analysis values, and red points indicate locations where the observed values are greater than the analysis values. The title lists the mean and standard deviation of the absolute value of the OMA values. 

The histogram plots OMA values on the x-axis and frequency density values on the y-axis. The title of the histogram lists the mean and standard deviation of the real value of the OMA values. 

.. |logo1| image:: https://raw.githubusercontent.com/wiki/ufs-community/land-DA_workflow/images/LandDAScatterPlot.png
   :alt: Map of snow depth in millimeters (observation minus analysis)

.. |logo2| image:: https://raw.githubusercontent.com/wiki/ufs-community/land-DA_workflow/images/LandDAHistogram.png 
   :alt: Histogram of snow depth in millimeters (observation minus analysis) on the x-axis and frequency density on the y-axis

.. _sample-plots:

.. list-table:: Snow Depth Plots for 2000-01-04

   * - |logo1|
     - |logo2|

.. note::

   There are many options for viewing plots, and instructions for this are highly machine dependent. Users should view the data transfer documentation for their system to secure copy files from a remote system (such as :term:`RDHPCS`) to their local system. 
   Another option is to download `Xming <https://sourceforge.net/projects/xming/>`_ (for Windows) or `XQuartz <https://www.xquartz.org/>`_ (for Mac), use the ``-X`` option when connecting to a remote system via SSH, and run:

   .. code-block:: console

      module load imagemagick
      display file_name.png

   where ``file_name.png`` is the name of the file to display/view. Depending on the system, users may need to install imagemagick and/or adjust other settings (e.g., for X11 forwarding). Users should contact their machine administrator with any questions. 
