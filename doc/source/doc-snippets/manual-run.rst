To run the experiment manually, issue a ``rocotorun`` command from the experiment directory: 

.. code-block:: console

   cd ../../exp_case/lnd_era5_warmstart_00/
   rocotorun -w land_analysis.xml -d land_analysis.db

Users will need to issue the ``rocotorun`` command multiple times. The tasks must be run in order, and ``rocotorun`` initiates the next task once its dependencies have completed successfully. 
