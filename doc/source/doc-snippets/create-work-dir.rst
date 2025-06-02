Users can either create a new directory for their Land DA work (e.g., ``landda``) or choose an existing directory, depending on preference. Then, users should navigate to this directory. For example, to create a new directory and navigate to it, run: 

.. code-block:: console

   mkdir /path/to/landda
   cd /path/to/landda

where ``/path/to/landda`` is the path to the directory where the user plans to run Land DA experiments (e.g., ``/Users/Joe.Schmoe/landda``). In the experiment configuration file, this directory is referred to as ``${exp_basedir}``. 

Optionally, users can save this directory path in an environment variable (e.g., ``$LANDDAROOT``) to avoid typing out full path names later. 

.. code-block:: console

   export LANDDAROOT=`pwd`

In this documentation, ``$LANDDAROOT`` is used, but users are welcome to choose another name for this variable if they prefer. 