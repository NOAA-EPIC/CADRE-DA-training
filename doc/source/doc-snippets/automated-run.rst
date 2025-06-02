To submit jobs automatically via crontab, users should navigate to the experiment directory and launch the workflow with the ``add`` argument: 

.. code-block:: console

   cd ../../exp_case/<EXP_CASE_NAME>
   ./launch_rocoto_wflow.sh add

where ``<EXP_CASE_NAME>`` is replaced with the actual name of the experiment directory (e.g., ``lnd_era5_warmstart_00/``).