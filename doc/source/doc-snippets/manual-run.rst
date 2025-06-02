To run the experiment manually, issue a ``rocotorun`` command from the experiment directory: 

.. code-block:: console

   cd ../../exp_case/<EXP_CASE_NAME>
   rocotorun -w land_analysis.xml -d land_analysis.db

where ``<EXP_CASE_NAME>`` is replaced with the actual name of the experiment directory (e.g., ``lnd_era5_warmstart_00/``).

Users will need to issue the ``rocotorun`` command multiple times. The tasks must be run in order, and ``rocotorun`` initiates the next task once its dependencies have completed successfully. 
