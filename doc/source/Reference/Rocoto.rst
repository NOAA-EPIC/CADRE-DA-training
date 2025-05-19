.. _RocotoInfo:

==================================
Rocoto Introductory Information
==================================
The tasks in the Land DA System are typically run using the Rocoto Workflow Manager (see :numref:`Table %s <WorkflowTasksTable>` for default tasks). Rocoto is a Ruby program that communicates with the batch system on an :term:`HPC` system to run and manage dependencies between the tasks. Rocoto submits jobs to the HPC batch system as the task dependencies allow and runs one instance of the workflow for a set of user-defined :term:`cycles <cycle>`. More information about Rocoto can be found on the `Rocoto Wiki <https://github.com/christopherwharrop/rocoto/wiki/documentation>`_.

The Land DA workflow is defined in a Jinja-enabled Rocoto XML template called ``land_analysis.xml``, which is generated using the contents of ``land_analysis.yaml`` as input to the Unified Workflow's :uw:`Rocoto tool <sections/user_guide/cli/tools/rocoto.html>`. Both files reside in the ``land-DA_workflow/parm`` directory. The completed XML file contains the workflow task names, parameters needed by the job scheduler, and task interdependencies. 

There are a number of Rocoto commands available to run and monitor the workflow; users can find more information in the complete `Rocoto documentation <http://christopherwharrop.github.io/rocoto/>`_. Descriptions and examples of commonly used commands are discussed below.

.. _RocotoRunCmd:

rocotorun
==========

The ``rocotorun`` command is used to run the workflow by submitting tasks to the batch system. It will automatically resubmit failed tasks and can recover from system outages without user intervention. The command takes the following format:

.. code-block:: console

   rocotorun -w /path/to/workflow/xml/file -d /path/to/workflow/database/file -v 10

where 				

* ``-w`` specifies the name of the workflow definition file. This must be an XML file (e.g., ``land_analysis.xml``).
* ``-d`` specifies the name of the database file that stores the state of the workflow (e.g., ``land_analysis.db``). The database file is a binary file created and used only by Rocoto. It does not need to exist when the command is initially run. 
* ``-v`` (optional) specified level of verbosity. If no level is specified, a level of 1 is used.

From the ``parm`` directory, the ``rocotorun`` command for the workflow would be:

.. code-block:: console

   rocotorun -w land_analysis.xml -d land_analysis.db

Users will need to include the absolute or relative path to these files when running the command from another directory. 

It is important to note that the ``rocotorun`` process is iterative; the command must be executed many times before the entire workflow is completed, usually every 1-10 minutes. More information on this command can be found in the `Rocoto documentation <http://christopherwharrop.github.io/rocoto/>`_.

The first time the ``rocotorun`` command is executed for a workflow, the files ``land_analysis.db`` and ``land_analysis_lock.db`` are created. There is usually no need for the user to modify these files. Each time the ``rocotorun`` command is executed, the last known state of the workflow is read from the ``land_analysis.db`` file, the batch system is queried, jobs are submitted for tasks whose dependencies have been satisfied, and the current state of the workflow is saved in ``land_analysis.db``. If there is a need to relaunch
the workflow from scratch, both database files can be deleted, and the workflow can be run by executing the ``rocotorun`` command
or the launch script (``launch_rocoto_wflow.sh``) multiple times.

.. _RocotoStatCmd:

rocotostat
===========

``rocotostat`` is a tool for querying the status of tasks in an active Rocoto workflow. Once the workflow has been started with the ``rocotorun`` command, Rocoto can check the status of the workflow using the ``rocotostat`` command:

.. code-block:: console

   rocotostat -w /path/to/workflow/xml/file -d /path/to/workflow/database/file

Concretely, this will look like: 

.. code-block:: console

   rocotostat -w land_analysis.xml -d land_analysis.db

Executing this command will generate a workflow status table similar to the following:

.. code-block:: console

   CYCLE                TASK                       JOBID        STATE   EXIT STATUS   TRIES   DURATION
   =========================================================================================================
   200001030000     prep_obs                    61746064       QUEUED             -       1        0.0
   200001030000     pre_anal   druby://10.184.3.62:41973   SUBMITTING             -       1        0.0
   200001030000     analysis                           -            -             -       -          -
   200001030000    post_anal                           -            -             -       -          -
   200001030000     forecast                           -            -             -       -          -
   200001030000   plot_stats                           -            -             -       -          -
   ================================================================================================================================
   200001040000     prep_obs   druby://10.184.3.62:41973   SUBMITTING             -       1        0.0
   200001040000     pre_anal                           -            -             -       -          -
   200001040000     analysis                           -            -             -       -          -
   200001040000    post_anal                           -            -             -       -          -
   200001040000     forecast                           -            -             -       -          -
   200001040000   plot_stats                           -            -             -       -          -
   
This table indicates that the ``prep_obs`` task for cycle 200001030000 was sent to the batch system and is now queued, while the ``pre_anal`` task for cycle 200001030000 and the ``prep_obs`` task for cycle 200001040000 are currently being submitted to the batch system. 

Note that issuing a ``rocotostat`` command without an intervening ``rocotorun`` command will not result in an updated workflow status table; it will print out the same table. It is the ``rocotorun`` command that updates the workflow database file (in this case ``land_analysis.db``, located in ``parm``). The ``rocotostat`` command reads the database file and prints the table to the screen. To see an updated table, the ``rocotorun`` command must be executed first, followed by the ``rocotostat`` command.

After issuing the ``rocotorun`` command several times (over the course of several minutes or longer, depending on the grid size and computational resources available), the output of the ``rocotostat`` command should look like this:

.. code-block:: console

          CYCLE             TASK        JOBID           STATE   EXIT STATUS   TRIES   DURATION
   ============================================================================================
   200001030000         prep_obs      1131735       SUCCEEDED            0       1        1.0
   200001030000         pre_anal      1131736       SUCCEEDED            0       1        5.0
   200001030000         analysis      1131754       SUCCEEDED            0       1       33.0
   200001030000        post_anal      1131811       SUCCEEDED            0       1       11.0
   200001030000         forecast      1131918       SUCCEEDED            0       1       31.0
   200001030000       plot_stats      1131944       SUCCEEDED            0       1       26.0
   ============================================================================================
   200001040000         prep_obs      1131737       SUCCEEDED            0       1        2.0
   200001040000         pre_anal      1131945       SUCCEEDED            0       1        3.0
   200001040000         analysis      1132118       SUCCEEDED            0       1       29.0
   200001040000        post_anal      1132174       SUCCEEDED            0       1       10.0
   200001040000         forecast      1132186       SUCCEEDED            0       1       31.0
   200001040000       plot_stats      1132319       RUNNING              -       1        0.0

When the workflow runs to completion, all tasks will be marked as SUCCEEDED. The log file for each task is located in ``$LANDDAROOT/ptmp/test/com/output/logs``. If any task fails, the corresponding log file can be checked for error messages. Optional arguments for the ``rocotostat`` command can be found in the `Rocoto documentation <http://christopherwharrop.github.io/rocoto/>`_.

.. _rocotocheck:

rocotocheck
============
Sometimes, issuing a ``rocotorun`` command will not cause the next task to launch. ``rocotocheck`` is a tool that can be used to query detailed information about a task or cycle in the Rocoto workflow. To determine why a particular task has not been submitted, the ``rocotocheck`` command can be used from the ``parm`` directory as follows:

.. code-block:: console

   rocotocheck -w land_analysis.xml -d land_analysis.db -c <YYYYMMDDHHmm> -t <taskname> 

where 

* ``-c`` is the cycle to query in YYYYMMDDHHmm format.
* ``-t`` is the task name (e.g., ``prep_obs``, ``analysis``, ``forecast``). 

The cycle and task names appear in the first and second columns of the table output by ``rocotostat``. Users will need to include the absolute or relative path to the workflow XML and database files when running the command from another directory.

A specific example is:

.. code-block:: console

   rocotocheck -w /Users/John.Doe/landda/land-DA_workflow/parm/land_analysis.xml -d /Users/John.Doe/landda/land-DA_workflow/parm/land_analysis.db -v 10 -c 200001040000 -t analysis

Running ``rocotocheck`` will result in output similar to the following:

.. code-block:: console
   :emphasize-lines: 9,34,35,47

   Task: analysis
      account: epic
      command: /work/noaa/epic/$USER/landda/land-DA_workflow/parm/task_load_modules_run_jjob.sh "analysis" "/work/noaa/epic/$USER/landda/land-DA_workflow" "orion"
      cores: 6
      cycledefs: cycled
      final: false
      jobname: analysis
      join: /work/noaa/epic/$USER/landda/ptmp/test/com/output/logs/run_gswp3/analysis_2000010400.log
      maxtries: 2
      name: analysis
      queue: batch
      throttle: 9999999
      walltime: 00:15:00
      environment
         ACCOUNT ==> epic
         ATMOS_FORC ==> gswp3
         COMROOT ==> /work/noaa/epic/$USER/landda/ptmp/test/com
         DATAROOT ==> /work/noaa/epic/$USER/landda/ptmp/test/tmp
         DAtype ==> letkfoi_snow
         HOMElandda ==> /work/noaa/epic/$USER/landda/land-DA_workflow
         JEDI_INSTALL ==> /work/noaa/epic/UFS_Land-DA_Dev/jedi_v7_stack1.6
         KEEPDATA ==> YES
         MACHINE ==> orion
         NPROCS_ANALYSIS ==> 6
         OBS_TYPES ==> GHCN
         PDY ==> 20000104
         RES ==> 96
         SCHED ==> slurm
         SNOWDEPTHVAR ==> snwdph
         TSTUB ==> oro_C96.mx100
         cyc ==> 00
         model_ver ==> v1.2.1
      dependencies
        pre_anal of cycle 200001040000 is SUCCEEDED

   Cycle: 200001040000
      Valid for this task: YES
      State: active
      Activated: 2024-07-05 17:44:40 UTC
      Completed: -
      Expired: -

   Job: 18347584
      State:  DEAD (FAILED)
      Exit Status: 1
      Tries: 2
      Unknown count: 0
      Duration: 70.0

This output shows that although all dependencies for this task are satisfied (see the dependencies section, highlighted above), it cannot run because its ``maxtries`` value (highlighted) is 2. Rocoto will attempt to launch it at most 2 times, and it has already been tried 2 times (note the ``Tries`` value, also highlighted).

The output of the ``rocotocheck`` command is often useful in determining whether the dependencies for a given task have been met. If not, the dependencies section in the output of ``rocotocheck`` will indicate this by stating that a dependency "is NOT satisfied".  

rocotorewind
=============
``rocotorewind`` is a tool that attempts to undo the effects of running a task. It is commonly used to rerun part of a workflow that has failed. If a task fails to run (the STATE is DEAD) and needs to be restarted, the ``rocotorewind`` command will rerun tasks in the workflow. The command line options are the same as those described for ``rocotocheck`` (in :numref:`Section %s <rocotocheck>`), and the general usage statement looks like this:

.. code-block:: console

   rocotorewind -w /path/to/workflow/xml/file -d /path/to/workflow/database/file -c <YYYYMMDDHHmm> -t <taskname> 

Running this command will edit the Rocoto database file ``land_analysis.db`` to remove evidence that the job has been run. ``rocotorewind`` is recommended over ``rocotoboot`` for restarting a task, since ``rocotoboot`` will force a specific task to run, ignoring all dependencies and throttle limits. The throttle limit, denoted by the variable ``cyclethrottle`` in the ``land_analysis.xml`` file, limits how many cycles can be active at one time. An example of how to use the ``rocotorewind`` command to rerun the forecast task from ``parm`` is:

.. code-block:: console

   rocotorewind -w land_analysis.xml -d land_analysis.db -v 10 -c 200001040000 -t forecast

rocotoboot
===========
``rocotoboot`` will force a specific task of a cycle in a Rocoto workflow to run. All dependencies and throttle limits are ignored, and it is generally recommended to use ``rocotorewind`` instead. An example of how to use this command to rerun the ``prep_obs`` task from ``parm`` is:

.. code-block:: console

   rocotoboot -w land_analysis.xml -d land_analysis.db -v 10 -c 200001040000 -t prep_obs

