To check on the job status, users on a system with a Slurm job scheduler may run: 

.. code-block:: console

   squeue -u $USER

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

Note that the status table printed by ``rocotostat`` only updates after each ``rocotorun`` command (whether issued manually or via cron automation). For each task, a log file is generated. These files are stored in ``$LANDDAROOT/ptmp/test_*/com/output/logs``. 

The experiment has successfully completed when all tasks say SUCCEEDED under STATE. Other potential statuses are: QUEUED, SUBMITTING, RUNNING, and DEAD. Users may view the log files to determine why a task may have failed.