Additionally, in the ``plot`` subdirectory, users will find a variety of plots for each cycle, including scatter plots (``hofx_omb_<obs_type>_YYYYMMDD_scatter.png``) and histograms (``hofx_omb_<obs_type>_YYYYMMDD_histogram.png``). 

The scatter plot is named OBS-BKG (i.e., Observation Minus Background [OMB]), and it depicts a map of snow depth results. Blue points indicate locations where the observed values are less than the background values, and red points indicate locations where the observed values are greater than the background values. The title lists the mean and standard deviation of the absolute value of the OMB values. 

The histogram plots OMB values on the x-axis and frequency density values on the y-axis. The title of the histogram lists the mean and standard deviation of the real value of the OMB values. 

.. |logo1| image:: https://raw.githubusercontent.com/wiki/ufs-community/land-DA_workflow/images/LandDAScatterPlot.png
   :alt: Map of snow depth in millimeters (observation minus background)

.. |logo2| image:: https://raw.githubusercontent.com/wiki/ufs-community/land-DA_workflow/images/LandDAHistogram.png 
   :alt: Histogram of snow depth in millimeters (observation minus background) on the x-axis and frequency density on the y-axis

.. list-table:: Snow Depth Plots for 2000-01-04

   * - |logo1|
     - |logo2|

.. note::

   There are many options for viewing plots, and instructions for this are highly machine dependent. Users should view the data transfer documentation for their system to secure copy files from a remote system (such as :term:`RDHPCS`) to their local system. 
   Another option is to download `Xming <https://sourceforge.net/projects/xming/>`_ (for Windows) or `XQuartz <https://www.xquartz.org/>`_ (for Mac), use the ``-X`` option when connecting to a remote system via SSH, and run:

   .. code-block:: console

      module load imagemagick
      display file_name.png

   where ``file_name.png`` is the name of the file to display/view. Depending on the system, users may need to install imagemagick and/or adjust other settings (e.g., for X11 forwarding). Users should contact their machine administrator with any questions. 
