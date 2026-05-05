As the experiment progresses, it will generate a number of directories to hold intermediate and output files. The structure of those files and directories appears below:

.. _land-da-dir-structure:

.. code-block:: console

   $LANDDAROOT (<exp_basedir>): Base directory
    ├── land-DA_workflow (<HOMElandda>): Home directory of the land DA workflow
    │     ├── jobs 
    │     ├── modulefiles
    │     ├── parm
    │     ├── scripts
    │     ├── sorc
    │     └── ush
    ├── exp_case
    │     └── $EXP_CASE_NAME
    │           ├── com_dir --> symlinked to ptmp/test_*/com/landda/v2.1.0
    │           ├── land_analysis.yaml
    │           ├── land_analysis.xml
    │           ├── launch_rocoto_wflow.sh
    │           ├── log_dir --> symlinked to ptmp/test_*/com/output/logs
    │           └── tmp_dir --> symlinked to ptmp/test_*/com/tmp
    └── ptmp (<PTMP>)
          └── test_* (<envir>)
                └── com (<COMROOT>)
                │     ├── landda (<NET>)
                │     │     └── vX.Y.Z (<model_ver>)
                │     │           └── landda.YYYYMMDD (<RUN>.<PDY>): Directory containing the output files
                │     │                 ├── datm
                │     │                 ├── hofx
                │     │                 ├── obs
                │     │                 └── plot
                │     └── output
                │           └── logs (<LOGDIR>): Directory containing the log files for the Rocoto workflow
                └── tmp (<DATAROOT>)
                     ├── [task_name].${PDY}${cyc}.<jobid> (<DATA>): Working directory for a specific task and cycle
                     └── DATA_SHARE
                           ├── INPUT_DATM 
                           ├── hofx: Directory containing the soft links to the results of the analysis task for plotting
                           ├── hofx_omb 
                           └── RESTART: Directory containing the soft links to the restart files for the next cycles

Each variable in parentheses and angle brackets (e.g., ``(<VAR>)``) is the name for the directory defined in the file ``land_analysis.yaml`` (derived from ``template.land_analysis.yaml`` or ``config.yaml``) or in the NCO Implementation Standards. For example, the ``<envir>`` variable is set to "test" (i.e., ``envir: "test"``) in ``template.land_analysis.yaml``. In the future, this directory structure will be further modified to meet the :nco:`NCO Implementation Standards<>`.

Check for the output files for each cycle in the experiment directory:

.. code-block:: console

   ls -l $LANDDAROOT/ptmp/test_*/com/landda/<model_ver>/landda.YYYYMMDD

where ``YYYYMMDD`` is the cycle date, and ``<model_ver>`` is the model version (currently v2.1.0 in the ``develop`` branch). The experiment should generate several restart files. 
