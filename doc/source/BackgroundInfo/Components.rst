.. _Components:

****************
Components
****************

The Land DA System assembles a variety of pre-processing, modeling, data assimilation, and workflow components. These components are documented within this User's Guide and supported through the `GitHub Discussions <https://github.com/ufs-community/ufs-srweather-app/discussions/categories/q-a>`_ forum. 

Pre-Processing/Data Conversion
================================

UFS_UTILS
-----------

The Land DA System includes the UFS_UTILS pre-processing software :ufs-utils:`chgres_cube <ufs_utils.html#chgres-cube>` to convert the raw external model data into initial conditions files in :term:`netCDF` format. These are needed as input to the :term:`FV3` component for the coldstart :term:`ATML` configuration. Additional information about the UFS pre-processing utilities can be found in the :ufs-utils:`UFS_UTILS Technical Documentation <>` and in the `UFS_UTILS Scientific Documentation <https://ufs-community.github.io/UFS_UTILS/>`_.

.. _calcfims:

calcfIMS.fd/land-SCF_proc
--------------------------

The Land DA System includes the ``calcfIMS.fd`` submodule, which points to the land surface processing (`land-SFC_proc <https://github.com/NOAA-EPIC/land-SCF_proc>`_) repository. This repository is forked from `NOAA-PSL/land-SFC_proc <https://github.com/NOAA-PSL/land-SCF_proc>`_, whose scientists originally developed the code. It primarily consists of code for processing :term:`IMS` ASCII files on the UFS model grid. As described in the repository's README.md file, the code requires IMS ASCII files and a resolution-specific IMS index file as input. As output, the code generates (1) snow cover fraction over land on the UFS model grid, and (2) snow depth (derived from the IMS snow cover fraction, using an inversion of the Noah model snow depletion curve).

IODA Converters
-----------------

The Land DA System accepts :term:`GHCN`, :term:`IMS`, or :term:`SFCSNO` data as input. The ``prep_data`` task then converts these data from their original format into the format needed by JEDI's :term:`UFO` and :term:`OOPS` components for data assimilation (see :numref:`Table %s: Workflow Tasks <WorkflowTasksTable>`). The Interface for Observation Data Access (:term:`IODA`) is the component of :term:`JEDI` that handles data processing for the data assimilation system (see :ref:`DA Components <da-components>` for more). The ``land-DA_workfow/ush`` directory contains scripts (e.g., ``ghcn_snod2ioda.py`` and ``imsfv3_scf2ioda.py``) that convert :term:`GHCN` and :term:`IMS` data to a JEDI-formatted NetCDF file using IODA. The :ref:`calcfIMS <calcfims>` executable mentioned above is an intermediate converter that converts the raw ASCII files to NetCDF format before performing additional JEDI formatting. 

tile2tile_converter
---------------------

The ``tile2tile_converter`` is a built-in tool that handles the conversion of variable names between the Land DA System's two main components: the UFS :term:`WM`'s land model (Noah-MP) and JEDI. :numref:`Table %s <t2tc>` indicates which variables are mismatched between Noah-MP and JEDI. 

.. _t2tc:

.. list-table:: Mismatched Variable Names
   :header-rows: 1

   * - ``tile2tile_converter`` Name
     - Description
     - Land model (Noah-MP)
     - JEDI (``sfc_data``)
   * - swe
     - Snow water equivalent
     - weasd
     - sheleg / weasdl
   * - snow_depth
     - Snow depth over land
     - snwdph
     - snwdph / snodl

The ``tile2tile_converter`` changes the variable names in two workflow tasks:

* In the ``pre_anal`` task, it changes from the variable names of UFS Weather Model Noah-MP component to those of JEDI
* In the ``post_anal`` task, it changes from the variable names of JEDI to those of UFS Weather Model Noah-MP component.

See :numref:`Table %s: Workflow Tasks <WorkflowTasksTable>` for more information on these workflow tasks. 

Modeling Components
=====================

The UFS Weather Model (WM)
----------------------------

The Unified Forecast System (:term:`UFS`) Weather Model (:term:`WM`) is a prognostic model that can be
used for short- and medium-range research and operational forecasts. In addition to its use in NOAA's operational forecast systems, the UFS WM is used in public UFS application releases, such as the most recent Land DA System and Short-Range Weather (SRW) Application releases. The WM assembles a variety of modeling components, including the :term:`FV3` atmospheric model, the :term:`Noah-MP` land surface model (LSM), and the data atmosphere (:term:`DATM`) model from the Community Data Models for Earth Predictive Systems (:term:`CDEPS`). A User's Guide for the UFS :term:`Weather Model` can be accessed :ufs-wm:`here <>`.


The FV3 Atmospheric Model
^^^^^^^^^^^^^^^^^^^^^^^^^^
The UFS WM's atmospheric model is the Finite-Volume Cubed-Sphere (:term:`FV3`) dynamical core (fv3atm). The :term:`dynamical core` is the computational part of a model that solves the equations of fluid motion. The Land DA System currently uses only the C96 resolution with 127 vertical levels. Additional information about the FV3 dynamical core can be found in the `scientific documentation <https://repository.library.noaa.gov/view/noaa/30725>`_, the `technical documentation <https://noaa-emc.github.io/FV3_Dycore_ufs-v2.0.0/html/index.html>`_, and on the `NOAA Geophysical Fluid Dynamics Laboratory website <https://www.gfdl.noaa.gov/fv3/>`_.

Model Physics
```````````````

The Common Community Physics Package (CCPP), described `here <https://dtcenter.org/community-code/common-community-physics-package-ccpp>`_, supports interoperable atmospheric physics and land surface model options. Atmospheric physics are a set of numerical methods describing small-scale processes such as clouds, turbulence, radiation, and their interactions. A full scientific description of CCPP v7.0.0 parameterizations and suites can be found in the `CCPP Scientific Documentation <https://dtcenter.ucar.edu/GMTB/v7.0.0/sci_doc/index.html>`_, and CCPP technical aspects are described in the :ccpp-techdoc:`CCPP Technical Documentation <>`. The model namelist has many settings beyond the physics options that can optimize various aspects of the model for use with each of the supported suites. Additional information on Stochastic Physics options is available :stochphys:`here <>`. 

.. _NoahMP:

Noah-MP
---------

The UFS Land DA System has been updated to build and run the UFS :ref:`Noah-MP <NoahMP>` land component of the UFS Weather Model. The land component makes use of a National Unified Operational Prediction Capability (:term:`NUOPC`) cap to interface with a coupled modeling system. 
This Noah-MP :term:`NUOPC cap` is able to create an :term:`ESMF` multi-tile grid by reading in a mosaic grid file. For the domain, the :term:`FMS` initializes reading and writing of the cubed-sphere tiled output. Then, the Noah-MP land component reads static information and initial conditions (e.g., surface albedo) and interpolates the data to the date of the simulation. The solar zenith angle is calculated based on the time information. 

In its original form, the offline Noah-MP LSM is a stand-alone, uncoupled model used to execute land surface simulations. In this traditional uncoupled mode, near-surface atmospheric :term:`forcing data` are required as input forcing. This LSM simulates soil moisture (both liquid and frozen), soil temperature, skin temperature, snow depth, snow water equivalent (SWE), snow density, canopy water content, and the energy flux and water flux terms of the surface energy balance and surface water balance.

Noah-MP uses: 

* a big-leaf approach with a separated vegetation canopy accounting for vegetation effects on surface energy and water balances, 
* a modified two-stream approximation scheme to include the effects of vegetation canopy gaps that vary with solar zenith angle and the canopy 3-D structure on radiation transfer, 
* a 3-layer physically-based snow model
* a more permeable frozen soil by separating a grid cell into a permeable fraction and impermeable fraction, 
* a simple groundwater model with a TOPMODEL-based runoff scheme, and 
* a short-term leaf phenology model. 

Noah-MP LSM enables a modular framework for diagnosing differences 
in process representation, facilitating ensemble forecasts and uncertainty 
quantification, and choosing process presentations appropriate for the application. 
Noah-MP developers designed multiple parameterization options for leaf dynamics, 
radiation transfer, stomatal resistance, soil moisture stress factor for stomatal 
resistance, aerodynamic resistance, runoff, snowfall, snow surface albedo, 
supercooled liquid water in frozen soil, and frozen soil permeability. 

The Noah-MP LSM has evolved through community efforts to pursue and refine a modern-era LSM suitable for use in the National Centers for Environmental Prediction (:term:`NCEP`) operational weather and climate prediction models. This collaborative effort continues with participation from entities such as NCAR, NCEP, NASA, and university groups. 

Noah-MP was originally implemented in the UFS via the :term:`CCPP` physics package and is currently being tested for operational use in GFSv17. 
Additionally, the UFS Weather Model now contains a Noah-MP land component, which is used as the land component in the Land DA System. 
Noah-MP has also been used operationally in the NOAA National Water Model (NWM) since 2016. Details about the model's physical parameterizations can be found in :cite:t:`NiuEtAl2011` (2011), and a full description of the model is available in the `Community Noah-MP Land Surface Modeling System Technical Description Version 5.0 <https://opensky.ucar.edu/islandora/object/technotes:599>`_. 

.. _da-components:

Data Assimilation
===================

The Joint Effort for Data assimilation Integration (:term:`JEDI`) is a unified and versatile :term:`data assimilation` (DA) system for Earth system prediction that can be run on a variety of platforms. In the Land DA System, JEDI software can be used to perform snow data assimilation using :term:`GHCN`, :term:`IMS`, or :term:`SFCSNO` data with :term:`LETKF` or :term:`3d-Var` algorithms. JEDI is developed by the Joint Center for Satellite Data Assimilation (`JCSDA <https://www.jcsda.org/>`_) and partner agencies, including NOAA. The core feature of JEDI is separation of concerns. The data assimilation update, observation selection and processing, and observation operators are all coded with no knowledge of or dependency on each other or on the forecast model. 

The Land DA System uses three main JEDI components: 
   
   * The Object-Oriented Prediction System (:jedi:`OOPS <inside/jedi-components/oops/index.html>`) for the data assimilation algorithm 
   * The Interface for Observation Data Access (:jedi:`IODA <inside/jedi-components/ioda/index.html>`) for the observation formatting and processing
   * The Unified Forward Operator (:jedi:`UFO <inside/jedi-components/ufo/index.html>`) for comparing model forecasts and observations 

These three components (and others) are conveniently packaged and provided via JCSDA's :term:`jedi-bundle`. Users are encouraged to visit the :jedi:`JEDI Documentation <inside/jedi-components/index.html>`. Users must build/install ``jedi-bundle`` prior to using the Land DA System; it does *not* come packaged in the Land DA System. 


apply_incr.fd
---------------

The Land DA System's ``apply_incr`` submodule points to NOAA PSL's `land-apply_jedi_incr <https://github.com/NOAA-PSL/land-apply_jedi_incr>`_ 

"Code to add DA increment generated by JEDI to UFS sfc_data restart. Currently, only option is to add snow depth increment to the Noah-MP land surface model. Above based on disaggregation code written by Mike Barlage."

.. COMMENT: Edit! 

      - land-apply_jedi_incr
      - Contains code that applies the JEDI-generated DA increment to UFS ``sfc_data`` restart 
      - https://github.com/NOAA-PSL/land-apply_jedi_incr

The Land DA System includes the ``calcfIMS.fd`` submodule, which points to the land surface processing (`land-SFC_proc <https://github.com/NOAA-EPIC/land-SCF_proc>`_) repository. This repository is forked from `NOAA-PSL/land-SFC_proc <https://github.com/NOAA-PSL/land-SCF_proc>`_, whose scientists originally developed the code. It primarily consists of code for processing :term:`IMS` ASCII files on the UFS model grid. As described in the repository's README.md file, the code requires IMS ASCII files and a resolution-specific IMS index file as input. As output, the code generates (1) snow cover fraction over land on the UFS model grid, and (2) snow depth (derived from the IMS snow cover fraction, using an inversion of the Noah model snow depletion curve).



Workflow
==========

The Land DA System has a portable, CMake-based build system that packages together the components necessary for running the end-to-end Land DA System, including: 

* The UFS Weather Model (particularly its :term:`FV3`, :term:`Noah-MP`, and :term:`CDEPS` components) 
* Data processing software (e.g., UFS_UTILS, tile2tile_converter, IODA converters)
* Configuration tools (:term:`JCB`, ``uwtools``)

Additional libraries necessary for the Land DA System must be installed separately via :term:`spack-stack` and :term:`jedi-bundle` unless users are working on a :ref:`supported platform <prerequisites>` or using a container. Once built, users can generate a Rocoto-based workflow that will run each task in the proper sequence (see :numref:`Chapter %s <RocotoInfo>` or the `Rocoto documentation <https://github.com/christopherwharrop/rocoto/wiki/Documentation>`_ for more information on Rocoto and workflow management). The workflow makes use of several configuration tools: 

* JEDI Configuration Builder
* Unified Workflow (UW) Tools

The Land DA System allows users to configure various elements of the workflow. For example, users can modify the start and end cycles for the experiment, the cycling frequency, and the duration of each forecast. It also allows for configuration of other elements of the workflow, such as data assimilation algorithm. More information on configurable variables is available in :numref:`Section %s <ConfigWorkflow>`.

.. COMMENT: Add data info in pre-processing section above instead?

JEDI Configuration Builder
----------------------------

The JEDI Configuration Builder (JCB) is a python package used to assemble information on :term:`JEDI` algorithms (e.g., letkf, 3dvar) and data assimilation types (e.g., snow, marine, atmosphere) into one convenient YAML file for use in data assimilation applications. The `jcb-algorithms <https://github.com/NOAA-EPIC/jcb-algorithms>`_ repository contains YAML algorithm files (e.g., LETKF, 3DVar) for JCB; these files contain the high-level configuration structure that is prescribed by the JEDI data assimilation system. The `jcb-gdas <https://github.com/NOAA-EPIC/jcb-gdas>`_ repository contains information for different types of analysis (e.g., snow, marine, atmosphere). 


Unified Workflow (UW) Tools (``uwtools``)
-------------------------------------------

``uwtools`` is a modern, open-source Python package that helps automate common tasks needed for many standard numerical weather prediction (NWP) workflows. It also provides drivers to automate the configuration and execution of UFS components, providing flexibility, interoperability, and usability to various UFS applications. The Unified Workflow (UW) tools are accessible from both a command-line interface (CLI) and a Python API. The CLI automates many core NWP workflow functions; the API supports all CLI operations and additionally provides access to in-memory objects to facilitate more novel use cases. These options allow users to integrate the package into pre-existing bash and Python scripts, in addition to providing some handy tools for use in day-to-day work with NWP systems. The ``uwtools`` Rocoto tool has been incorporated into the Land DA System. More details about UW tools can be found in the `uwtools GitHub repository <https://github.com/ufs-community/uwtools>`_ and in the :uw:`UW Documentation <>`.

Utility Scripts
-----------------

The ``land-DA_workflow/ush`` directory contains several utility scripts that perform useful workflow functions. 

.. COMMENT: Add details! 
   tile2tile_converter, IODA converting scripts, and python scripts
   
