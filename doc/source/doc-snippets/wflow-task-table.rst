Each Land DA experiment includes multiple tasks that must be run in order to satisfy the dependencies of later tasks. These tasks are housed in the :term:`J-job <j-jobs>` scripts contained in the ``jobs`` directory. 

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
