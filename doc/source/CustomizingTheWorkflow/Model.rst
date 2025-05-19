.. _Model:

*****************************************
Input/Output Files for the Noah-MP Model
*****************************************

This chapter provides practical information on input files and parameters for the Noah-MP Land Surface Model (LSM).
For background information on the Noah-MP LSM, see :numref:`Section %s <NoahMP>` of the Introduction. 

.. _InputFiles:

Input Files 
**************

The UFS land model requires multiple input files to run, including static datasets (fix files containing climatological information, terrain, and land use data), initial conditions files, and forcing files. 
Users may reference the `Community Noah-MP Land Surface Modeling System Technical Description Version 5.0 <https://opensky.ucar.edu/islandora/object/technotes:599>`_ (2023) for a detailed technical description of certain elements of the Noah-MP model.

In Noah-MP, the static file(s) and initial conditions file(s) specify model parameters. 
These files are publicly available in the `Land DA data bucket <https://registry.opendata.aws/noaa-ufs-land-da/>`_. 
Users can download the data and untar the file via the command line:

.. _TarFile:

.. code-block:: console

   wget https://noaa-ufs-land-da-pds.s3.amazonaws.com/develop-20241024/inputs.tar.gz
   tar xvfz inputs.tar.gz

For data specific to the latest release (|latestr|), users can run: 

.. code-block:: console
   
   wget https://noaa-ufs-land-da-pds.s3.amazonaws.com/current_land_da_release_data/v2.0.0/LandDAInputDatav2.0.0.tar.gz
   tar xvfz LandDAInputDatav2.0.0.tar.gz

These files and their parameters are described in the following subsections.


.. _view-netcdf-files:

Viewing netCDF Files
======================

Users can view file information, variables, and notes for NetCDF files using the ``ncdump`` module. On Level 1 platforms, users can load the Land DA environment from ``land-DA_workflow`` as described in :numref:`Section %s <config-wflow>`. 

.. include:: ../doc-snippets/load-env.rst

Then, users can run ``ncdump -h path/to/filename.nc``, where ``path/to/filename.nc`` is replaced with the path to the file. For example, on Orion, users might run: 

.. code-block:: console

   module load netcdf/4.7.0
   ncdump -h /work/noaa/epic/UFS_Land-DA_Dev/inputs/NOAHMP_IC/ufs-land_C96_init_fields.tile1.nc


On other systems, users can load a compiler, MPI, and NetCDF modules before running the ``ncdump`` command above. For example: 

.. code-block:: console

   module load intel/2022.1.2 impi/2022.1.2 netcdf/4.7.0
   ncdump -h /path/to/inputs/NOAHMP_IC/ufs-land_C96_init_fields.tile1.nc

Users may need to modify the ``module load`` command to reflect modules that are available on their system. 

.. _datm-lnd-input-files:

Input Files for the ``DATM`` + ``LND`` Configuration with GSWP3 data
======================================================================

With the integration of the UFS Noah-MP land component into the Land DA System, model forcing options have been enhanced so that users can run the UFS land component (:term:`LND`) with the data atmosphere component (:term:`DATM`). Updates provide a new analysis option on the cubed-sphere native grid using :term:`GSWP3` forcing data to run a cycled experiment for 2000-01-03 to 2000-01-04. An artificial GHCN snow depth observation is provided for data assimilation (see :numref:`Section %s <observation-data>` for more on GHCN files). The GHCN observations will be extended in the near future. 

On Level 1 platforms, the requisite data are pre-staged at the locations listed in :numref:`Section %s <Level1Data>`. The data are also publicly available via the `Land DA Data Bucket <https://registry.opendata.aws/noaa-ufs-land-da/>`_. 

Forcing Files
---------------

:term:`Forcing files<forcing data>` for the land component configuration come from the Global Soil Wetness Project Phase 3 dataset. They are located in the ``inputs/DATM_input_data/gswp3`` directory (downloaded :ref:`above <InputFiles>`).

.. code-block:: console 

   clmforc.GSWP3.c2011.0.5x0.5.Prec.1999-12.nc
   clmforc.GSWP3.c2011.0.5x0.5.Prec.2000-01.nc
   clmforc.GSWP3.c2011.0.5x0.5.Solr.1999-12.nc
   clmforc.GSWP3.c2011.0.5x0.5.Solr.2000-01.nc
   clmforc.GSWP3.c2011.0.5x0.5.TPQWL.1999-12.nc
   clmforc.GSWP3.c2011.0.5x0.5.TPQWL.2000-01.nc
   clmforc.GSWP3.c2011.0.5x0.5.TPQWL.SCRIP.210520_ESMFmesh.nc
   fv1.9x2.5_141008_ESMFmesh.nc
   topodata_0.9x1.25_USGS_070110_stream_c151201.nc
   topodata_0.9x1.SCRIP.210520_ESMFmesh.nc

These files provide atmospheric forcing data related to precipitation, solar radiation, longwave radiation, temperature, pressure, winds, humidity, topography, and mesh data. 

Noah-MP Initial Conditions
----------------------------

The offline Land DA System currently only supports snow DA. 
The initial conditions files include the initial state variables that are required for the UFS land snow DA to begin a cycling run. The data must be provided in :term:`netCDF` format. 

By default, on Level 1 systems and in the Land DA data bucket, the initial conditions files are located at ``inputs/NOAHMP_IC/ufs-land_C96_init_fields.tile*.nc`` (downloaded :ref:`above <InputFiles>`). Each file corresponds to one of the six tiles of the `global FV3 grid <https://www.gfdl.noaa.gov/fv3/fv3-grids/>`_.  

The files contain the following data:             

.. list-table:: *Variables specified in the initial conditions file ufs-land_C96_init_fields.tile*.nc*
   :header-rows: 1

   * - Variables
     - Long Name
     - Units 
   * - time(time)
     - "time"
     - "seconds since 1970-01-01 00:00:00"
   * - geolat(lat, lon)
     - "latitude"
     - "degrees_north"
   * - geolon(lat, lon)
     - "longitude"
     - "degrees_east"
   * - snow_water_equivalent(time, lat, lon)
     - "snow water equivalent"
     - "mm"
   * - snow_depth(time, lat, lon)
     - "snow depth"
     - "m"
   * - canopy_water(time, lat, lon)
     - "canopy surface water"
     - "mm"
   * - skin_temperature(time, lat, lon)
     - "surface skin temperature"
     - "K"
   * - soil_temperature(time, soil_levels, lat, lon)
     - "soil temperature"
     - "K"
   * - soil_moisture(time, soil_levels, lat, lon)
     - "volumetric soil moisture"
     - "m3/m3"
   * - soil_liquid(time, soil_levels, lat, lon)
     - "volumetric soil liquid"
     - "m3/m3"


FV3_fix_tiled Files
---------------------

The UFS land component also requires a series of tiled static (fix) files that will be used by the component model. These files contain information on maximum snow albedo, slope type, soil color and type, substrate temperature, vegetation greenness and type, and orography (grid and land mask information). These files are located in the ``inputs/FV3_fix_tiled/C96`` directory (downloaded :ref:`above <InputFiles>`). 

.. code-block:: console

   C96.facsf.tile*.nc
   C96_grid.tile*.nc
   C96.maximum_snow_albedo.tile*.nc 
   C96.slope_type.tile*.nc
   C96.snowfree_albedo.tile*.nc
   C96.soil_type.tile*.nc
   C96.soil_color.tile*.nc
   C96.substrate_temperature.tile*.nc
   C96.vegetation_greenness.tile*.nc
   C96.vegetation_type.tile*.nc
   grid_spec.nc
   oro_C96.mx100.tile*.nc

The ``C96_grid.tile*.nc`` files contain grid information for tiles 1-6 at C96 grid resolution. The ``grid_spec.nc`` file contains information on the mosaic grid. 

.. note:: 

   ``grid_spec.nc`` and ``C96.mosaic.nc`` are the same file under different names and may be used interchangeably. 

