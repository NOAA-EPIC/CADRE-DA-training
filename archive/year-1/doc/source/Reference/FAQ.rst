.. _FAQ:

*********************************
Frequently Asked Questions (FAQ)
*********************************

.. contents::
   :depth: 2
   :local:

.. _DeadTask:

My tasks went DEAD. Why might this be?
========================================

The most common reason for the first few tasks to go DEAD is an improper path in the ``parm_xml.yaml`` configuration file. 
In particular, ``exp_basedir`` must be set to the directory above ``land-DA_workflow``. For example, if ``land-DA_workflow`` resides at ``Users/Jane.Doe/landda/land-DA_workflow``, then ``exp_basedir`` must be set to ``Users/Jane.Doe/landda``. After correcting ``parm_xml.yaml``, users will need to regenerate the workflow XML by running: 

.. code-block:: console

   uw template render --input-file templates/template.land_analysis.yaml --values-file parm_xml.yaml --output-file land_analysis.yaml
   uw rocoto realize --input-file land_analysis.yaml --output-file land_analysis.xml

Then, rewind the DEAD tasks as described :ref:`below <RestartTask>` using ``rocotorewind``, and use ``rocotorun``/``rocotostat`` to advance/check on the workflow (see :numref:`Section %s <automated-run>` for how to do this). 

If the first few tasks run successfully, but future tasks go DEAD, users will need to check the experiment log files, located at ``$EXP_BASEDIR/ptmp/test/com/output/logs``. It may also be useful to check that the JEDI directory and other paths and values are correct in ``parm_xml.yaml``. 


.. _RestartTask:

How do I restart a DEAD task?
=============================

On platforms that utilize Rocoto workflow software (including Hera and Orion), if something goes wrong with the workflow, a task may end up in the DEAD state:

.. code-block:: console

   $ rocotostat -w land_analysis.xml -d land_analysis.db

   CYCLE                TASK     JOBID        STATE   EXIT STATUS   TRIES   DURATION
   =======================================================================================
   200001030000     prep_obs  61746034    SUCCEEDED             0       1       11.0
   200001030000     pre_anal  61746035    SUCCEEDED             0       1       13.0
   200001030000     analysis  61746081    SUCCEEDED             0       1       76.0
   200001030000    post_anal  61746109    SUCCEEDED             0       1        4.0
   200001030000   plot_stats  61746110    SUCCEEDED             0       1       70.0
   200001030000     forecast  61746128         DEAD           256       1          -
   200001030000   plot_stats         -            -             -       -          -


This means that the DEAD task has not completed successfully, so the workflow has stopped. Once the issue has been identified and fixed (e.g., by referencing the log files in ``$LANDDAROOT/ptmp/test/com/output/logs``), users can rewind, or "undo," the failed task using the ``rocotorewind`` command:

.. code-block:: console

   rocotorewind -w land_analysis.xml -d land_analysis.db -v 10 -c 200001030000 -t forecast

where ``-c`` specifies the cycle date (first column of ``rocotostat`` output) and ``-t`` represents the task name
(second column of ``rocotostat`` output). This will set the number of tries to 0, as though the task has not been run. After using ``rocotorewind``, the next time ``rocotorun`` is used to advance the workflow, the job will be resubmitted.

