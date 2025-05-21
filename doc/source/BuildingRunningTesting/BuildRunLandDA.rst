.. _BuildRunLandDA:

***********************************************
Land DA Workflow (Hera/Orion/Hercules/Gaea-C6)
***********************************************

This chapter provides instructions for building and running the Unified Forecast System (:term:`UFS`) Land DA System using a Jan. 19-20, 2025 00z sample :term:`LND` :term:`warmstart` case using :term:`ERA5` and :term:`IMS` data and the 3D-Var algorithm with the UFS Noah-MP land component and data atmosphere (:term:`DATM`) component.

This case corresponds to the January 2025 Gulf Coast Blizzard, which brought unprecedented snowfall to the entire Gulf Coast. Leading up to the event, the polar vortex stretched far south and met with unusually warm Gulf waters. In response, the National Weather Service (NWS) issued a series of winter storm warnings, extreme cold warnings, and even blizzard warnings --- the first ever in some areas. New Orleans, LA received a record 8 inches of snow, and the surrounding coastal areas likewise saw record-breaking snowfall and cold temperatures. 

.. attention::
   
   These steps are designed for use on :ref:`Level 1 <LevelsOfSupport>` systems (e.g., Hera, Orion) and may require significant changes on other systems. It is recommended that users on other systems run the containerized version of Land DA. Users may reference :numref:`Chapter %s: Containerized Land DA Workflow <Container>` for instructions.

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

.. attention:: 

   When working with a release branch, be sure to follow instructions in the release branch documentation. View the `v2.0.0 release documentation here <https://land-da-workflow.readthedocs.io/en/release-public-v2.0.0/>`_. 

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
     - /scratch2/NAGAPE/epic/UFS_Land-DA_v2.1/inputs
   * - Hercules & Orion
     - /work/noaa/epic/UFS_Land-DA_v2.1/inputs
   * - Gaea-C6
     - /gpfs/f6/bil-fire8/world-shared/UFS_Land-DA_v2.1/inputs

Users who have difficulty accessing the data on Hera, Orion, Hercules, or Gaea-C6 may download it according to the instructions in :numref:`Section %s <GetDataC>`. Its subdirectories are soft-linked to the ``land-DA_workflow/fix`` directory by the build script (``sorc/app_build.sh``); when downloading new data, it should be placed in or linked to the ``fix`` directory.

.. _generate-wflow:

Set Up the Workflow
==============================

Generate the experiment directory by running: 

.. code-block:: console

   ./setup_wflow_env.py -p=<platform>

where ``<platform>`` is ``hera``, ``orion``, ``hercules``, or ``gaeac6``.

If the command runs without issue, this script will print override messages, experiment details, and "0 errors found" messages to the console, similar to the following excerpts: 

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

Run the Experiment
********************

To run the experiment, users can automate job submission via :term:`crontab` or submit tasks manually via ``rocotorun``. 

.. _wflow-overview:

Workflow Overview
==================

.. include:: ../doc-snippets/wflow-task-table.rst


.. _automated-run:

Automated Run
==================

To automate task submission, users must be on a system where :term:`cron` is available. On Orion, cron is only available on the orion-login-1 node, and likewise on Hercules, it is only available on hercules-login-1, so users will need to work on those nodes when running cron jobs on Orion/Hercules.

.. include:: ../doc-snippets/automated-run.rst

To check the status of the experiment, see :numref:`Section %s <VerifySuccess>` on tracking experiment progress.

.. note::

   If users run into issues with the launch script, they can run ``conda deactivate`` before running the launch script. 

.. _manual-run:

Manual Submission
==================

.. include:: ../doc-snippets/manual-run.rst

Details on checking experiment status are provided in the :ref:`next section <VerifySuccess>`.

.. _VerifySuccess:

Track Progress
=================

.. include:: ../doc-snippets/track-progress.rst

.. _check-output:

Check Experiment Output
=========================

.. include:: ../doc-snippets/check-output.rst

.. _plotting:

Plotting Results
-----------------

.. include:: ../doc-snippets/plotting.rst