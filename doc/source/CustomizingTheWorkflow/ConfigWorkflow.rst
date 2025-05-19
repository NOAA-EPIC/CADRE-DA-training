.. _ConfigWorkflow:

***************************************************
Available Workflow Configuration Parameters
***************************************************

To run the Land DA System, users must create an experiment configuration file (named ``land_analysis.yaml`` by default) that combines the default values in ``template.land_analysis.yaml`` with user-specified values from ``parm_xml.yaml``. Currently, ``template.land_analysis.yaml`` contains most of the experiment-specific information, such as forecast/cycle dates, while ``parm_xml.yaml`` contains user/machine-specific settings, such as data directory locations. To help the user, sample ``parm_xml_<machine>.yaml`` configuration files have been included in the ``parm`` directory for use on Hera, Orion, and Hercules. The ``template.land_analysis.yaml`` contains reasonable experiment default values that work on those machines. The contents of these files can be used as the starting point from which to generate a variety of experiment configurations for Land DA. 

The following is a list of the parameters included in the ``land_analysis.yaml`` file (and derived from ``template.land_analysis.yaml`` and ``parm_xml.yaml``). For each parameter, the default value and a brief description are provided. 

.. _wf-attributes:

Workflow Attributes (``attrs:``)
=================================

Attributes pertaining to the overall workflow are defined in the ``attrs:`` section under ``workflow:``. For example: 

.. code-block:: console 

   workflow:
     attrs:
       realtime: false
       scheduler: slurm
       cyclethrottle: 24
       taskthrottle: 24

``realtime:`` (Default: false)
   Indicates whether it is a realtime run (true) or a retrospective run (false). Valid values: ``true`` | ``false``

``scheduler:`` (Default: slurm)
   The job scheduler to use on the specified machine. Valid values: ``"slurm"``. Other options may work with a container but have not been tested: ``"pbspro"`` | ``"lsf"`` | ``"lsfcray"`` | ``"none"``

``cyclethrottle:`` (Default: 24)
   The number of cycles that can be active at one time. Valid values: Integers > 0.

``taskthrottle:`` (Default: 24)
   The number of tasks that can be active at one time. Valid values: Integers > 0.

.. _wf-cycledef:

Workflow Cycle Definition (``cycledef``)
==========================================

Cycling information is defined in the ``cycledef:`` section under ``workflow:``. Each cycle definition starts with a hyphen (``-``) and has information on cycle attributes (``attrs:``) and a cycle specification (``spec:``). For example: 

.. code-block:: console 

   workflow:
     cycledef:
       - attrs:
           group: cycled
         spec: 201912210000 201912220000 24:00:00

``attrs:``
   Attributes of ``cycledef``. Includes ``group:`` but may also include ``activation_offset:``. See the :rocoto:`Rocoto Documentation <>` for more information. 

   ``group:``
      The group attribute allows users to assign a set of cycles to a particular group. The group tag can later be used to control which tasks are run for which cycles. See the :rocoto:`Rocoto Documentation <>` for more information. 

``spec:`` 
   The cycle is defined using the "start stop step" method, with the cycle start date listed first in YYYMMDDHHmm format, followed by the end date and then the step in HH:mm:SS format (e.g., ``201912210000 201912220000 24:00:00``).


.. _wf-entities:

Workflow Entities
===================

Entities are constants that can be referred to throughout the workflow using the ampersand (``&``) prefix and semicolon (``;``) suffix (e.g., ``&MACHINE;``) to avoid defining the same constants repetitively in each workflow task. For example, in a ``land_analysis.yaml`` created on Orion, the following entities are defined: 

.. code-block:: console 

   workflow:
     entities:
       MACHINE: "orion"
       SCHED: "slurm"
       ACCOUNT: "epic"
       EXP_BASEDIR: "/work/noaa/epic/{USER}/landda_test"
       JEDI_INSTALL: "/work/noaa/epic/UFS_Land-DA_Dev/jedi_v7_stack1.6"
       WARMSTART_DIR: "/work/noaa/epic/UFS_Land-DA_Dev/inputs/DATA_RESTART"
       ATMOS_FORC: "gswp3"
       RES: "96"
       NPROCS_ANALYSIS: "6"
       FCSTHR: "24"
       DT_ATMOS: "900"
       DT_RUNSEQ: "3600"
       NPROCS_FORECAST: "26"
       NPROCS_FORECAST_ATM: "12"
       NPROCS_FORECAST_LND: "12"
       LND_LAYOUT_X: "1"
       LND_LAYOUT_Y: "2"
       LND_OUTPUT_FREQ_SEC: "21600"
       NNODES_FORECAST: "1"
       NPROCS_PER_NODE: "26"
       OBSDIR: ""
       OBSDIR_SUBDIR: ""
       OBS_TYPES: "GHCN"
       DAtype: "letkfoi_snow"
       TSTUB: "oro_C96.mx100"
       WE2E_TEST: "YES"
       WE2E_ATOL: "1e-7"
       WE2E_LOG_FN: "we2e.log"
       NET: "landda"
       envir: "test"
       model_ver: "v2.0.0"
       RUN: "landda"
       HOMElandda: "&EXP_BASEDIR;/land-DA_workflow"
       PTMP: "&EXP_BASEDIR;/ptmp"
       COMROOT: "&PTMP;/&envir;/com"
       DATAROOT: "&PTMP;/&envir;/tmp"
       KEEPDATA: "YES"
       LOGDIR: "&COMROOT;/output/logs;"
       LOGFN_SUFFIX: "<cyclestr>_@Y@m@d@H.log</cyclestr>"
       PDY:  "<cyclestr>@Y@m@d</cyclestr>"
       cyc: "<cyclestr>@H</cyclestr>"
       DATADEP_FILE1: "<cyclestr>&WARMSTART_DIR;/ufs_land_restart.@Y-@m-@d_@H-00-00.tile1.nc</cyclestr>"
       DATADEP_FILE2: "<cyclestr>&WARMSTART_DIR;/ufs_land_restart.@Y-@m-@d_@H-00-00.nc</cyclestr>"
       DATADEP_FILE3: "<cyclestr>&DATAROOT;/DATA_SHARE/RESTART/ufs_land_restart.@Y-@m-@d_@H-00-00.tile1.nc</cyclestr>"
       DATADEP_FILE4: "<cyclestr>&DATAROOT;/DATA_SHARE/RESTART/ufs_land_restart.@Y-@m-@d_@H-00-00.nc</cyclestr>"

``MACHINE:`` (Default: "{{ machine }}")
   The machine (a.k.a. platform or system) on which the workflow will run. The actual value is derived from the ``parm_xml_<machine>.yaml`` file. Currently supported platforms are listed in :numref:`Section %s <LevelsOfSupport>`. Valid values: ``"hera"`` | ``"orion"`` | ``"hercules"``

``SCHED:`` (Default: "slurm")
   The job scheduler to use (e.g., Slurm) on the specified ``MACHINE``. Valid values: ``"slurm"``. Other options may work with a container but have not been tested: ``"pbspro"`` | ``"lsf"`` | ``"lsfcray"`` | ``"none"``

``ACCOUNT:`` (Default: "{{ account }}")
   An account where users can charge their compute resources on the specified ``MACHINE``. To determine an appropriate ``ACCOUNT`` field on a system with a Slurm job scheduler, users may run the ``saccount_params`` command to display account details. On other systems, users may run the ``groups`` command, which will return a list of projects that the user has permissions for. Not all of the listed projects/groups have an HPC allocation, but those that do are potentially valid account names. The actual value used in the workflow is derived from the ``parm_xml_<machine>.yaml`` file. 

``EXP_BASEDIR:`` (Default: "{{ exp_basedir }}")
   The full path to the parent directory of ``land-DA_workflow`` (i.e., ``$LANDDAROOT`` in the documentation). The actual value is derived from the ``parm_xml_<machine>.yaml`` file. 

``JEDI_INSTALL:`` (Default: "{{ jedi_install }}")
   The path to the JEDI |skylabv| installation. Derived from the ``parm_xml_<machine>.yaml`` file. The actual value is derived from the ``parm_xml_<machine>.yaml`` file. 

``WARMSTART_DIR:`` (Default: "{{ warmstart_dir }}")
   The path to restart files for a warmstart experiment. The actual value is derived from the ``parm_xml_<machine>.yaml`` file. 

``ATMOS_FORC:`` (Default: "gswp3")
   Type of atmospheric forcing data used. Valid values: ``"gswp3"``

``RES:`` (Default: "96")
   Resolution of FV3 grid. Currently, only C96 resolution is supported. 

``FCSTHR:`` (Default: "24")
   Specifies the length of each forecast in hours. Valid values: Integers > 0.

``NPROCS_ANALYSIS:`` (Default: "6")
   Number of processors for the analysis task. 

``DT_ATMOS:`` (Default: "900")
   The main integration time step of the atmospheric component of the UFS Weather Model (in seconds). This is the time step for the outermost atmospheric model loop and must be a positive integer value. It corresponds to the frequency at which the physics routines and the top level dynamics routine are called. (Note that one call to the top-level dynamics routine results in multiple calls to the horizontal dynamics, tracer transport, and vertical dynamics routines; see the `FV3 dycore scientific documentation <https://repository.library.noaa.gov/view/noaa/30725>`_ for details.) 
   
``DT_RUNSEQ:`` (Default: "6")
   Time interval of run sequence (coupling interval) between the model components of the UFS Weather Model (in seconds).

``NPROCS_FORECAST:`` (Default: "26")
   Total number of processes for the FORECAST task.

``NPROCS_FORECAST_ATM:`` (Default: "12")
   Number of processes for the atmospheric model component (DATM) in the FORECAST task.

``NPROCS_FORECAST_LND:`` (Default: "12")
   Number of processes for the land model component (Noah-MP) in the FORECAST task.

``LND_LAYOUT_X:`` (Default: "1")
   Number of processes in the x direction per tile for the land model component.

``LND_LAYOUT_Y:`` (Default: "2")
   Number of processes in the y direction per tile for the land model component.

``LND_OUTPUT_FREQ_SEC:`` (Default: "21600")
   Output frequency of the land model component (in seconds).

``NNODES_FORECAST:`` (Default: "1")
   Number of nodes for the FORECAST task.

``NPROCS_PER_NODE:`` (Default: "26")
   Number of processes per node for the FORECAST task.
 
``OBSDIR:`` (Default: "")
   The path to the directory where DA fix files are located. In ``scripts/exlandda_prep_obs.sh``, this value is set to ``${FIXlandda}/DA`` unless the user specifies a different path in ``template.land_analysis.yaml``. 

``OBSDIR_SUBDIR:`` (Default: "")
   The path to the directories where different types of fix data (e.g., ERA5, GSWP3, GTS, NOAH-MP) are located. In ``scripts/exlandda_prep_obs.sh``, this value is set based on the type(s) of data requested. The user may choose to set a different value. 

``OBS_TYPES:`` (Default: "GHCN")
   Specifies the observation type. Format is "Obs1" "Obs2". Currently, only GHCN observation data is available. 

``DAtype:`` (Default: "letkfoi_snow")
   Type of data assimilation. Valid values: ``letkfoi_snow``. Currently, Land DA only performs snow DA. As the application expands, more options may be added. 

``TSTUB:`` (Default: "oro_C96.mx100")
   Specifies the file stub/name for orography files in ``TPATH``. This file stub is named ``oro_C${RES}`` for atmosphere-only orography files and ``oro_C{RES}.mx100`` for atmosphere and ocean orography files. When Land DA is compiled with ``sorc/app_build.sh``, the subdirectories of the fix files should be linked into the ``fix`` directory, and orography files can be found in ``fix/FV3_fix_tiled/C96``. 

``WE2E_TEST:`` (Default: "{{ we2e_test }}"/"NO")
   Flag to turn on the workflow end-to-end (WE2E) test. When WE2E_TEST="YES", the result files from the experiment are compared to the test baseline files, located in ``fix/test_base/we2e_com``. If the results are within the tolerance set (via ``WE2E_ATOL``) at the end of the three main tasks --- ``analysis``, ``forecast``, and ``post_anal`` --- then the experiment passes. The actual value is derived from the ``parm_xml_<machine>.yaml`` file but preset to "NO" in that file. Valid values: ``"YES"`` | ``"NO"``

``WE2E_ATOL:`` (Default: "1e-7")
   Tolerance of the WE2E test

``WE2E_LOG_FN:`` (Default: "we2e.log")
   Name of the WE2E test log file

``DATADEP_FILE1:`` (Default: "<cyclestr>&WARMSTART_DIR;/ufs_land_restart.@Y-@m-@d_@H-00-00.tile1.nc</cyclestr>")
   File name for the dependency check for the task ``pre_anal``. The ``pre_anal`` task is triggered only when one or more of the ``DATADEP_FILE#`` files exists. Otherwise, the task will not be submitted.

``DATADEP_FILE2:`` (Default: "<cyclestr>&WARMSTART_DIR;/ufs_land_restart.@Y-@m-@d_@H-00-00.nc</cyclestr>")
   File name for the dependency check for the task ``pre_anal``. The ``pre_anal`` task is triggered only when one or more of the ``DATADEP_FILE#`` files exists. Otherwise, the task will not be submitted.

``DATADEP_FILE3:`` (Default: "<cyclestr>&DATAROOT;/DATA_SHARE/RESTART/ufs_land_restart.@Y-@m-@d_@H-00-00.tile1.nc</cyclestr>")
   File name for the dependency check for the task ``pre_anal``. The ``pre_anal`` task is triggered only when one or more of the ``DATADEP_FILE#`` files exists. Otherwise, the task will not be submitted.

``DATADEP_FILE4:`` (Default: "<cyclestr>&DATAROOT;/DATA_SHARE/RESTART/ufs_land_restart.@Y-@m-@d_@H-00-00.nc</cyclestr>")
   File name for the dependency check for the task ``pre_anal``. The ``pre_anal`` task is triggered only when one or more of the ``DATADEP_FILE#`` files exists. Otherwise, the task will not be submitted.
    
.. _nco-dir-entities:

NCO Directory Structure Entities
----------------------------------

Standard environment variables are defined in the NCEP Central Operations :nco:`WCOSS Implementation Standards <ImplementationStandards.v11.0.0.pdf>` document (pp. 4-5). These variables are used in forming the path to various directories containing input, output, and workflow files. For a visual aid, see the :ref:`Land DA Directory Structure Diagram <land-da-dir-structure>`. 

``HOMElandda:`` (Default: "&EXP_BASEDIR;/land-DA_workflow")
   The location of the :github:`land-DA_workflow <>` clone. 

``PTMP:`` (Default: "&EXP_BASEDIR;/ptmp")
   Product temporary (PTMP) experiment output space. This directory is used to mimic the operational file structure and contains all of the files and subdirectories used by or generated by the experiment. By default, it is a sibling to the ``land-DA_workflow`` directory. 

``envir:`` (Default: "test")
   The run environment. Set to “test” during the initial testing phase, “para” when running in parallel (on a schedule), and “prod” in production. In operations, this is the operations root directory (aka ``$OPSROOT``). 

``COMROOT:`` (Default: "&PTMP;/&envir;/com")
   ``com`` root directory, which contains input/output data on current system. 

``NET:`` (Default: "landda")
   Model name (first level of ``com`` directory structure)

``model_ver:`` (Default: "v2.0.0")
   Version number of package in three digits (e.g., v#.#.#); second level of ``com`` directory

``RUN:`` (Default: "landda")
   Name of model run (third level of ``com`` directory structure). In general, same as ``${NET}``.

``DATAROOT:`` (Default: "&PTMP;/&envir;/tmp")
   Directory location for the temporary working directories for running jobs. By default, this is a sibling to the ``$COMROOT`` directory and is located at ``ptmp/test/tmp``. 

``KEEPDATA:`` (Default: "YES")
   Flag to keep data ("YES") or not ("NO") that is copied to the ``$DATAROOT`` directory during the forecast experiment.

``LOGDIR:`` (Default: "&COMROOT;/output/logs;")
   Path to the directory containing log files for each workflow task. 

``LOGFN_SUFFIX:`` (Default: "<cyclestr>_@Y@m@d@H.log</cyclestr>")
   The cycle suffix appended to each task's log file. It will be rendered in the form ``_YYYYMMDDHH.log``. For example, the ``prep_obs`` task log file for the Jan. 4, 2000 00z cycle would be named: ``prep_obs_2000010400.log``.

``PDY:``  (Default: "<cyclestr>@Y@m@d</cyclestr>")
   Date in YYYYMMDD format.

``cyc:`` (Default: "<cyclestr>@H</cyclestr>")
   Cycle time in GMT hours, formatted HH.

.. _wf-log:

Workflow Log
==============

Information related to overall workflow progress is defined in the ``log:`` section under ``workflow:``:

.. code-block:: console

   workflow:
     log: "&LOGDIR;/workflow.log"

``log:`` (Default: "&LOGDIR;/workflow.log")
   Path and name of Rocoto log file(s).

.. _wf-tasks:

Workflow Tasks
================

The workflow is divided into discrete tasks, and details of each task are defined within the ``tasks:`` section under ``workflow:``. 

.. code-block:: console

   workflow:
     tasks:
       task_prep_obs:
       task_pre_anal:
       task_analysis:
       task_post_anal:
       task_plot_stats:
       task_forecast:

Each task may contain attributes (``attrs:``), just as in the overarching ``workflow:`` section. Instead of entities, each task contains an ``envars:`` section to define environment variables that must be passed to the task when it is executed. Any task dependencies are listed under the ``dependency:`` section. Additional details, such as ``jobname:``, ``walltime:``, and ``queue:`` may also be set within a specific task. 

The following subsections explain any variables that have not already been explained/defined above. 

.. _sample-task:

Sample Task: Analysis Task (``task_analysis``)
------------------------------------------------

This section walks users through the structure of the analysis task (``task_analysis``) to explain how configuration information is provided to the ``land_analysis.yaml`` file for each task. Since each task has a similar structure, common information is explained in this section. Variables unique to a particular task are defined in their respective ``task_`` sections below. 

Parameters for a particular task are set in the ``workflow.tasks.task_<name>:`` section of the ``template.land_analysis.yaml`` file. For example, settings for the analysis task are provided in the ``task_analysis:`` section of ``template.land_analysis.yaml``. The following is an excerpt of the ``task_analysis:`` section of ``template.land_analysis.yaml``:

.. code-block:: console

   workflow:
     tasks: 
       task_analysis:
         attrs:
           cycledefs: cycled
           maxtries: 2
         envars:
           OBS_TYPES: "&OBS_TYPES;"
           MACHINE: "&MACHINE;"
           SCHED: "&SCHED;"
           ACCOUNT: "&ACCOUNT;"
           EXP_NAME: "&EXP_NAME;"
           RES: "&RES;"
           TSTUB: "&TSTUB;"
           WE2E_TEST: "&WE2E_TEST;"
           WE2E_ATOL: "&WE2E_ATOL;"
           WE2E_LOG_FN: "&WE2E_LOG_FN;"
           LOGDIR: "&LOGDIR;
           model_ver: "&model_ver;"
           HOMElandda: "&HOMElandda;"
           COMROOT: "&COMROOT;"
           DATAROOT: "&DATAROOT;"
           KEEPDATA: "&KEEPDATA;"
           PDY: "&PDY;"
           cyc: "&cyc;"
           DAtype: "&DAtype;"
           NPROCS_ANALYSIS: "&NPROCS_ANALYSIS;"
           JEDI_INSTALL: "&JEDI_INSTALL;"
         account: "&ACCOUNT;"
         command: '&HOMElandda;/parm/task_load_modules_run_jjob.sh "analysis" "&HOMElandda;" "&MACHINE;"'
         jobname: analysis
         nodes: "1:ppn=&NPROCS_ANALYSIS;"
         walltime: 00:15:00
         queue: batch
         join: "&LOGDIR;/analysis&LOGFN_SUFFIX;"
         dependency:
           taskdep:
             attrs:
               task: pre_anal

.. _task-attributes:

Task Attributes (``attrs:``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``attrs:`` section for each task includes the ``cycledefs:`` attribute and the ``maxtries:`` attribute. 

``cycledefs:`` (Default: cycled)
   A comma-separated list of ``cycledef:`` group names. A task with a ``cycledefs:`` group ID will be run only if its group ID matches one of the workflow's ``cycledef:`` group IDs. 

``maxtries:`` (Default: 2)
   The maximum number of times Rocoto can resumbit a failed task. 

.. _task-envars:

Task Environment Variables (``envars``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``envars:`` section for each task reuses many of the same variables and values defined as ``entities:`` for the overall workflow. These values are needed for each task, but setting them individually is error-prone. Instead, a specific workflow task can reference workflow entities using the ``&VAR;`` syntax. For example, to set the ``ACCOUNT:`` value in ``task_analysis:`` to the value of the workflow ``ACCOUNT:`` entity, the following statement can be added to the task's ``envars:`` section:

.. code-block:: console

   task_analysis:
      envars:
        ACCOUNT: "&ACCOUNT;"

For most workflow tasks, whatever value is set in the ``workflow.entities:`` section should be reused/referenced in other tasks. For example, the ``MACHINE`` variable must be defined for each task, and users cannot switch machines mid-workflow. Therefore, users should set the ``MACHINE`` variable in the ``workflow.entities:`` section and reference that definition in each workflow task. For example:

.. code-block:: console

   workflow:
     entities:
       MACHINE: "orion"
     tasks: 
       task_prep_obs:
         envars:
           MACHINE: "&MACHINE;"
       task_pre_anal:
         envars:
           MACHINE: "&MACHINE;"
       task_analysis:
         envars:
           MACHINE: "&MACHINE;"
       ...
       task_forecast:
         envars:
           MACHINE: "&MACHINE;"

.. _misc-tasks:

Miscellaneous Task Values
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The authoritative :rocoto:`Rocoto documentation <>` discusses a number of miscellaneous task attributes in detail. A brief overview is provided in this section. 

.. code-block:: console
   
   workflow:
     tasks: 
       task_analysis:
         account: "&ACCOUNT;"
         command: '&HOMElandda;/parm/task_load_modules_run_jjob.sh "analysis" "&HOMElandda;" "&MACHINE;"'
         jobname: analysis
         nodes: "1:ppn=&NPROCS_ANALYSIS;"
         walltime: 00:15:00
         queue: batch
         join: "&LOGDIR;/analysis&LOGFN_SUFFIX;"

``ACCOUNT:`` (Default: "&ACCOUNT;")
   An account where users can charge their compute resources on the specified ``MACHINE``. This value is typically the same for each task, so the default is to reuse the value set in the :ref:`Workflow Entities <wf-entities>` section. 

``command:`` (Default: ``'&HOMElandda;/parm/task_load_modules_run_jjob.sh "analysis" "&HOMElandda;" "&MACHINE;"'``)
   The command that Rocoto will submit to the batch system to carry out the task's work. 

``jobname:`` (Default: analysis)
   Name of the task/job (default will vary based on the task). 

``nodes:`` (Default: "1:ppn=&NPROCS_ANALYSIS;")
   Number of nodes required for the task (default will vary based on the task). 

``walltime:`` (Default: 00:15:00)
   Time allotted for the task (default will vary based on the task). 

``queue:`` (Default: batch)
   The batch system queue or "quality of servie" (QOS) that Rocoto will submit the task to for execution.

``join:`` (Default: "&LOGDIR;/analysis&LOGFN_SUFFIX;")
   The full path to the task's log file, which records output from ``stdout`` and ``stderr``. 

Some tasks include a ``cores:`` value instead of a ``nodes:`` value. For example: 

``cores:`` (Default: 1)
   The number of cores required for the task. 

.. _task-dependencies:

Dependencies
^^^^^^^^^^^^^^

The ``dependency:`` section of a task defines what prerequisites must be met for the task to run. In the case of ``task_analysis:``, it must be run after the ``pre_anal`` task. Therefore, the dependecy section lists a task dependency (``taskdep:``). 

.. code-block:: console
   
   workflow:
     tasks: 
       task_analysis:
         dependency:
           taskdep:
             attrs:
               task: pre_anal

Other tasks may list data or time dependencies. For example, the pre-analysis task (``task_pre_anal:``) requires at least one of four possible data files to be available before it can run. 

.. code-block:: console
   
   workflow:
     tasks: 
       task_pre_anal:
         dependency:
           or:
             datadep_file1:
               attrs:
                 age: 5
               value: "&DATADEP_FILE1;"
             datadep_file2:
               attrs:
                 age: 5
               value: "&DATADEP_FILE2;"
             datadep_file3:
               attrs:
                 age: 5
               value: "&DATADEP_FILE3;"
             datadep_file4:
               attrs:
                 age: 5
               value: "&DATADEP_FILE4;"

For details on dependencies (e.g., ``attrs:``, ``age:``, ``value:`` tags), view the authoritative :rocoto:`Rocoto documentation <>`.

.. _prep-obs:

Observation Preparation Task (``task_prep_obs``)
--------------------------------------------------

Parameters for the observation preparation task are set in the ``task_prep_obs:`` section of the ``template.land_analysis.yaml`` file. Most task variables are the same as the defaults set and defined in the :ref:`Workflow Entities <wf-entities>` section. Variables common to all tasks are discussed in more detail in the :ref:`Sample Task <sample-task>` section, although the default values may differ. 

.. code-block:: console

   workflow:
     tasks: 
       task_prep_obs:
         attrs:
           cycledefs: cycled
           maxtries: 2
         envars:
           OBSDIR: "&OBSDIR;"
           OBSDIR_SUBDIR: "&OBSDIR_SUBDIR;"
           OBS_TYPES: "&OBS_TYPES;"
           MACHINE: "&MACHINE;"
           SCHED: "&SCHED;"
           ACCOUNT: "&ACCOUNT;"
           ATMOS_FORC: "&ATMOS_FORC;"
           model_ver: "&model_ver;"
           HOMElandda: "&HOMElandda;"
           COMROOT: "&COMROOT;"
           DATAROOT: "&DATAROOT;"
           KEEPDATA: "&KEEPDATA;"
           PDY: "&PDY;"
           cyc: "&cyc;"
         account: "&ACCOUNT;"
         command: '&HOMElandda;/parm/task_load_modules_run_jjob.sh "prep_obs" "&HOMElandda;" "&MACHINE;"'
         jobname: prep_obs
         cores: 1
         walltime: 00:02:00
         queue: batch
         join: "&LOGDIR;/prep_obs&LOGFN_SUFFIX;"

.. _pre-anal:

Pre-Analysis Task (``task_pre_anal``)
---------------------------------------

Parameters for the pre-analysis task are set in the ``task_pre_anal:`` section of the ``template.land_analysis.yaml`` file. Most task variables are the same as the defaults set and defined in the :ref:`Workflow Entities <wf-entities>` section. Variables common to all tasks are discussed in more detail in the :ref:`Sample Task <sample-task>` section, although the default values may differ. 

.. code-block:: console

   workflow:
     tasks: 
       task_pre_anal:
         attrs:
           cycledefs: cycled
           maxtries: 2
         envars:
           MACHINE: "&MACHINE;"
           SCHED: "&SCHED;"
           ACCOUNT: "&ACCOUNT;"
           RES: "&RES;"
           TSTUB: "&TSTUB;"
           WARMSTART_DIR: "&WARMSTART_DIR;"
           model_ver: "&model_ver;"
           RUN: "&RUN;"
           HOMElandda: "&HOMElandda;"
           COMROOT: "&COMROOT;"
           DATAROOT: "&DATAROOT;"
           KEEPDATA: "&KEEPDATA;"
           PDY: "&PDY;"
           cyc: "&cyc;"
         account: "&ACCOUNT;"
         command: '&HOMElandda;/parm/task_load_modules_run_jjob.sh "pre_anal" "&HOMElandda;" "&MACHINE;"'
         jobname: pre_anal
         cores: 1
         walltime: 00:05:00
         queue: batch
         join: "&LOGDIR;/pre_anal&LOGFN_SUFFIX;"
         dependency:
           or:
             datadep_file1:
               attrs:
                 age: 5
               value: "&DATADEP_FILE1;"
             datadep_file2:
               attrs:
                 age: 5
               value: "&DATADEP_FILE2;"
             datadep_file3:
               attrs:
                 age: 5
               value: "&DATADEP_FILE3;"
             datadep_file4:
               attrs:
                 age: 5
               value: "&DATADEP_FILE4;"


.. _analysis:

Analysis Task (``task_analysis``)
-----------------------------------

Parameters for the analysis task are set in the ``task_analysis:`` section of the ``template.land_analysis.yaml`` file. Most are the same as the defaults set in the :ref:`Workflow Entities <wf-entities>` section. The ``task_analysis:`` task is explained fully in the :ref:`Sample Task <sample-task>` section. 

.. _post-analysis:

Post-Analysis Task (``task_post_anal``)
-----------------------------------------

Parameters for the post analysis task are set in the ``task_post_anal:`` section of the ``template.land_analysis.yaml`` file. Most task variables are the same as the defaults set and defined in the :ref:`Workflow Entities <wf-entities>` section. Variables common to all tasks are discussed in more detail in the :ref:`Sample Task <sample-task>` section, although the default values may differ.

.. code-block:: console

   workflow:
     tasks: 
       task_post_anal:
         attrs:
           cycledefs: cycled
           maxtries: 2
         envars:
           MACHINE: "&MACHINE;"
           SCHED: "&SCHED;"
           ACCOUNT: "&ACCOUNT;"
           RES: "&RES;"
           TSTUB: "&TSTUB;"
           model_ver: "&model_ver;"
           RUN: "&RUN;"
           HOMElandda: "&HOMElandda;"
           COMROOT: "&COMROOT;"
           DATAROOT: "&DATAROOT;"
           KEEPDATA: "&KEEPDATA;"
           PDY: "&PDY;"
           cyc: "&cyc;"
           FCSTHR: "&FCSTHR;"
         account: "&ACCOUNT;"
         command: '&HOMElandda;/parm/task_load_modules_run_jjob.sh "post_anal" "&HOMElandda;" "&MACHINE;"'
         jobname: post_anal
         cores: 1
         walltime: 00:05:00
         queue: batch
         join: "&LOGDIR;/post_anal&LOGFN_SUFFIX;"
         dependency:
           taskdep:
             attrs:
               task: analysis

.. _plot-stats:

Plotting Task (``task_plot_stats``)
-------------------------------------

Parameters for the plotting task are set in the ``task_plot_stats:`` section of the ``template.land_analysis.yaml`` file. Most task variables are the same as the defaults set and defined in the :ref:`Workflow Entities <wf-entities>` section. Variables common to all tasks are discussed in more detail in the :ref:`Sample Task <sample-task>` section, although the default values may differ. 

.. code-block:: console

   workflow:
     tasks: 
       task_plot_stats:
         attrs:
           cycledefs: cycled
           maxtries: 2
         envars:
           MACHINE: "&MACHINE;"
           SCHED: "&SCHED;"
           ACCOUNT: "&ACCOUNT;"
           model_ver: "&model_ver;"
           RUN: "&RUN;"
           HOMElandda: "&HOMElandda;"
           COMROOT: "&COMROOT;"
           DATAROOT: "&DATAROOT;"
           KEEPDATA: "&KEEPDATA;"
           PDY: "&PDY;"
           cyc: "&cyc;"
         account: "&ACCOUNT;"
         command: '&HOMElandda;/parm/task_load_modules_run_jjob.sh "plot_stats" "&HOMElandda;" "&MACHINE;"'
         jobname: plot_stats
         cores: 1
         walltime: 00:10:00
         queue: batch
         join: "&LOGDIR;/plot_stats&LOGFN_SUFFIX;"
         dependency:
           taskdep:
             attrs:
               task: analysis

.. _forecast:

Forecast Task (``task_forecast``)
----------------------------------

Parameters for the forecast task are set in the ``task_forecast:`` section of the ``template.land_analysis.yaml`` file. Most task variables are the same as the defaults set and defined in the :ref:`Workflow Entities <wf-entities>` section. Variables common to all tasks are discussed in more detail in the :ref:`Sample Task <sample-task>` section, although the default values may differ. 

.. code-block:: console

   workflow:
     tasks: 
       task_forecast:
         attrs:
           cycledefs: cycled
           maxtries: 2
         envars:
           OBS_TYPES: "&OBS_TYPES;"
           MACHINE: "&MACHINE;"
           SCHED: "&SCHED;"
           ACCOUNT: "&ACCOUNT;"
           ATMOS_FORC: "&ATMOS_FORC;"
           RES: "&RES;"
           WARMSTART_DIR: "&WARMSTART_DIR;"
           model_ver: "&model_ver;"
           HOMElandda: "&HOMElandda;"
           COMROOT: "&COMROOT;"
           DATAROOT: "&DATAROOT;"
           KEEPDATA: "&KEEPDATA;"
           LOGDIR: "&LOGDIR;"
           PDY: "&PDY;"
           cyc: "&cyc;"
           DAtype: "&DAtype;"
           FCSTHR: "&FCSTHR;"
           DT_ATMOS: "&DT_ATMOS;"
           DT_RUNSEQ: "&DT_RUNSEQ;"
           NPROCS_FORECAST: "&NPROCS_FORECAST;"
           NPROCS_FORECAST_ATM: "&NPROCS_FORECAST_ATM;"
           NPROCS_FORECAST_LND: "&NPROCS_FORECAST_LND;"
           LND_LAYOUT_X: "&LND_LAYOUT_X;"
           LND_LAYOUT_Y: "&LND_LAYOUT_Y;"
           LND_OUTPUT_FREQ_SEC: "&LND_OUTPUT_FREQ_SEC;"
           NNODES_FORECAST: "&NNODES_FORECAST;"
           NPROCS_PER_NODE: "&NPROCS_PER_NODE;"
         account: "&ACCOUNT;"
         command: '&HOMElandda;/parm/task_load_modules_run_jjob.sh "forecast" "&HOMElandda;" "&MACHINE;"'
         jobname: forecast
         nodes: "1:ppn=&NPROCS_FORECAST;:ppn=&NPROCS_PER_NODE;"
         walltime: 00:30:00
         queue: batch
         join: "&LOGDIR;/forecast&LOGFN_SUFFIX;"
         dependency:
           taskdep:
             attrs:
               task: post_anal
