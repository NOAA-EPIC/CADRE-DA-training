Each Land DA experiment includes multiple tasks that must be run in order to satisfy the dependencies of later tasks. These tasks are housed in the :term:`J-job <j-jobs>` scripts contained in the ``jobs`` directory. 

.. list-table:: *J-job Tasks in the Land DA Workflow*
   :header-rows: 1

   * - J-job Task
     - Description
     - Application/Configuration
   * - PREP_DATA
     - Prepares the observation / :term:`DATM` forcing data files
     - LND/ATML
   * - FCST_IC 
     - Generates initial conditions (IC) files for the ATML configuration only
     - ATML
   * - JCB
     - Generates :term:`JEDI` configuration YAML file
     - LND/ATML
   * - PRE_ANAL
     - Transfers the snow depth data from the restart files to the surface data files
     - LND
   * - ANALYSIS
     - Runs JEDI and adds the increment to the surface data files
     - LND/ATML
   * - POST_ANAL
     - Transfers the JEDI snow depth result from the surface data files to the restart files
     - LND/ATML
   * - FORECAST
     - Runs the forecast model
     - LND/ATML
   * - PLOT_STATS
     - Plots the results of the ANALYSIS and FORECAST tasks
     - LND/ATML
