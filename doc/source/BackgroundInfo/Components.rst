.. _Components:

****************
Components
****************

The Land DA System assembles a variety of modeling, data assimilation, pre-processing, and workflow components. These components are documented within this User's Guide and supported through the `GitHub Discussions <https://github.com/ufs-community/land-DA_workflow/discussions/categories/q-a>`_ forum. 

.. _modeling-components:

Modeling Components
=====================

The UFS Weather Model (WM)
----------------------------

The Unified Forecast System (:term:`UFS`) Weather Model (:term:`WM`) is a prognostic model that can be
used for short- and medium-range research and operational forecasts. In addition to its use in NOAA's operational forecast systems, the UFS WM is used in public UFS application releases, such as the most recent Land DA System and Short-Range Weather (SRW) Application releases. The WM assembles a variety of modeling components, including the :term:`FV3` atmospheric model, the :term:`Noah-MP` land surface model (LSM), and the data atmosphere (:term:`DATM`) model from the Community Data Models for Earth Predictive Systems (:term:`CDEPS`) component. A User's Guide for the UFS WM can be accessed :ufs-wm:`here <>`.

.. _fv3-component:

The FV3 Atmospheric Model
^^^^^^^^^^^^^^^^^^^^^^^^^^
The UFS WM's atmospheric model is the Finite-Volume Cubed-Sphere (:term:`FV3`) dynamical core (`fv3atm <https://github.com/NOAA-EMC/fv3atm>`_). The :term:`dynamical core` is the computational part of a model that solves the equations of fluid motion. The Land DA System currently uses only the C96 resolution with 127 vertical levels. Additional information about the FV3 dynamical core can be found in the `scientific documentation <https://repository.library.noaa.gov/view/noaa/30725>`_, the `technical documentation <https://noaa-emc.github.io/FV3_Dycore_ufs-v2.0.0/html/index.html>`_, and on the `NOAA Geophysical Fluid Dynamics Laboratory (GFDL) website <https://www.gfdl.noaa.gov/fv3/>`_.

Model Physics
```````````````

The Common Community Physics Package (CCPP), described `here <https://dtcenter.org/community-code/common-community-physics-package-ccpp>`_, supports interoperable atmospheric physics and land surface model options. Atmospheric physics are a set of numerical methods describing small-scale processes such as clouds, turbulence, radiation, and their interactions. A full scientific description of CCPP v7.0.0 parameterizations and suites can be found in the `CCPP Scientific Documentation <https://dtcenter.ucar.edu/GMTB/v7.0.0/sci_doc/index.html>`_, and CCPP technical aspects are described in the :ccpp-techdoc:`CCPP Technical Documentation <>`. 

.. _NoahMP:

Noah-MP
^^^^^^^^

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

The UFS Weather Model now contains a Noah-MP land component, which is used as the land component in the Land DA System. Details about the model's physical parameterizations can be found in :cite:t:`NiuEtAl2011` (2011), and a full description of the model is available in the `Community Noah-MP Land Surface Modeling System Technical Description Version 5.0 <https://opensky.ucar.edu/islandora/object/%3A3912>`_. 

.. _da-components:

Data Assimilation
===================

The Joint Effort for Data assimilation Integration (:term:`JEDI`) is a unified and versatile :term:`data assimilation` (DA) system for Earth system prediction that can be run on a variety of platforms. In the Land DA System, JEDI software can be used to perform snow data assimilation using :term:`GHCN`, :term:`IMS`, or :term:`SFCSNO` data with :term:`LETKF` or :term:`3D-Var` algorithms. JEDI is developed by the Joint Center for Satellite Data Assimilation (`JCSDA <https://www.jcsda.org/>`_) and partner agencies, including NOAA. 

The Land DA System uses three main JEDI components: 
   
   * The Object-Oriented Prediction System (:jedi:`OOPS <inside/jedi-components/oops/index.html>`) for the data assimilation algorithm 
   * The Interface for Observation Data Access (:jedi:`IODA <inside/jedi-components/ioda/index.html>`) for the observation formatting and processing
   * The Unified Forward Operator (:jedi:`UFO <inside/jedi-components/ufo/index.html>`) for comparing model forecasts and observations 

These three components (and others) are conveniently packaged and provided via JCSDA's :term:`jedi-bundle`. Users must build/install ``jedi-bundle`` prior to using the Land DA System if they are *not* working on a :ref:`Level 1 <level1>` platform; ``jedi-bundle`` does *not* come packaged in the Land DA System. Users are encouraged to visit the :jedi:`JEDI Documentation <inside/jedi-components/index.html>` for more information. 

apply_incr.fd
---------------

The Land DA System's ``apply_incr`` submodule points to NOAA PSL's `land-apply_jedi_incr <https://github.com/NOAA-PSL/land-apply_jedi_incr>`_ repository. This repository contains code to add the DA increment generated by JEDI to the ``sfc_data`` restart file. A `DA increment <https://www.meted.ucar.edu/bom/mdata_assim/navmenu.php?tab=1&page=3-7-0&type=flash>`_, or analysis increment, is the difference between what the model predicted and what the DA objective analysis computes as the best fit between the model state and the observations. Replacing the model state directly with the objective analysis can cause artificial shocks that will propagate through the system, so DA systems require code that slowly nudges the model state towards the analysis by applying part of the increment at a time as the new forecast steps forward in time. 

.. _preprocessing:

Pre-Processing/Data Conversion
================================

The Land DA System makes use of various data pre-processing and conversion tools so that users have options for different input data sources and different Land DA configurations. 

.. _ufs-utils:

UFS_UTILS
-----------

The Land DA System includes the UFS_UTILS pre-processing software :ufs-utils:`chgres_cube <ufs_utils.html#chgres-cube>` to convert the raw external model data into initial conditions files in :term:`netCDF` format. These are needed as input to the :term:`FV3` component for the coldstart :term:`ATML` configuration. Additional information about the UFS pre-processing utilities can be found in the :ufs-utils:`UFS_UTILS Technical Documentation <>` and in the `UFS_UTILS Scientific Documentation <https://ufs-community.github.io/UFS_UTILS/>`_.

.. _calcfims:

calcfIMS.fd/land-SCF_proc
--------------------------

The Land DA System includes the ``calcfIMS.fd`` submodule, which points to the land surface processing repository (`NOAA-EPIC/land-SFC_proc <https://github.com/NOAA-EPIC/land-SCF_proc>`_). This repository is forked from `NOAA-PSL/land-SFC_proc <https://github.com/NOAA-PSL/land-SCF_proc>`_, where the code was originally developed. It primarily consists of code for processing :term:`IMS` ASCII files on the UFS model grid. As described in the repository's README.md file, the code requires IMS ASCII files and a resolution-specific IMS index file as input. As output, the code generates (1) snow cover fraction over land on the UFS model grid, and (2) snow depth (derived from the IMS snow cover fraction, using an inversion of the Noah model snow depletion curve).

.. _ioda-converters:

IODA Converters
-----------------

The Land DA System accepts :term:`GHCN`, :term:`IMS`, or :term:`SFCSNO` data as input. The ``prep_data`` task then converts these data from their original format into the format needed by JEDI's :term:`UFO` and :term:`OOPS` components for data assimilation (see :ref:`Workflow Tasks <wflow-overview>`). The Interface for Observation Data Access (:term:`IODA`) is the component of :term:`JEDI` that handles data processing for the data assimilation system (see :ref:`DA Components <da-components>` for more). The ``land-DA_workfow/ush`` directory contains scripts (e.g., ``ghcn_snod2ioda.py`` and ``imsfv3_scf2ioda.py``) that convert :term:`GHCN` and :term:`IMS` data to a JEDI-formatted NetCDF file using IODA. The :ref:`calcfIMS <calcfims>` executable mentioned above is an intermediate converter that converts the raw ASCII files to NetCDF format before performing additional JEDI formatting. 

.. _t2tc:

tile2tile_converter
---------------------

The ``tile2tile_converter`` is a built-in tool that handles the conversion of variable names between the Land DA System's two main components: the UFS :term:`WM`'s land model (Noah-MP) and JEDI. :numref:`Table %s <t2tc-vars>` indicates which variables are mismatched between Noah-MP and JEDI. 

.. _t2tc-vars:

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

* In the ``pre_anal`` task, it changes from the variable names of UFS Weather Model Noah-MP component to those of JEDI.
* In the ``post_anal`` task, it changes from the variable names of JEDI to those of the UFS WM Noah-MP component.

See :numref:`Section %s: Workflow Tasks <wflow-overview>` for more information on these workflow tasks. 


Workflow
==========

The Land DA System has a portable, CMake-based build system that packages together the components necessary for running the end-to-end Land DA System, including: 

* The UFS Weather Model (particularly its :term:`FV3`, :term:`Noah-MP`, and :term:`CDEPS` components) 
* Data processing software (e.g., UFS_UTILS, tile2tile_converter, IODA converters)
* Configuration tools (:term:`JEDI` Configuration Builder, Unified Workflow Tools)

Additional libraries necessary for the Land DA System must be installed separately via :term:`spack-stack` and :term:`jedi-bundle` unless users are working on a :ref:`supported platform <prerequisites>` or using a container. Once built, users can generate a Rocoto-based workflow that will run each task in the proper sequence (see :numref:`Chapter %s <RocotoInfo>` or the `Rocoto documentation <https://github.com/christopherwharrop/rocoto/wiki/Documentation>`_ for more information on Rocoto and workflow management). The workflow makes use of several configuration tools: 

* JEDI Configuration Builder
* Unified Workflow (UW) Tools

The Land DA System allows users to configure various elements of the workflow. For example, users can modify the start and end cycles for the experiment, the cycling frequency, and the duration of each forecast. It also allows for configuration of other elements of the workflow, such as data assimilation algorithm. More information on configurable variables is available in :numref:`Section %s <ConfigWorkflow>`.

.. _jcb-component:

JEDI Configuration Builder
----------------------------

The JEDI Configuration Builder (JCB) is a python package used to assemble information on :term:`JEDI` algorithms (e.g., letkf, 3dvar) and data assimilation types (e.g., snow, marine, atmosphere) into one convenient YAML file for use in data assimilation applications. The `jcb-algorithms <https://github.com/NOAA-EPIC/jcb-algorithms>`_ repository contains YAML algorithm files (e.g., LETKF, 3DVar) for JCB; these files contain the high-level configuration structure that is prescribed by the JEDI data assimilation system. The `jcb-gdas <https://github.com/NOAA-EPIC/jcb-gdas>`_ repository contains information for different types of analysis (e.g., snow, marine, atmosphere).  


Unified Workflow (UW) Tools (``uwtools``)
-------------------------------------------

``uwtools`` is a modern, open-source Python package that helps automate common tasks needed for many standard numerical weather prediction (NWP) workflows. It also provides drivers to automate the configuration and execution of UFS components, providing flexibility, interoperability, and usability to various UFS applications. The Unified Workflow (UW) tools are accessible from both a command-line interface (CLI) and a Python API. The CLI automates many core NWP workflow functions; the API supports all CLI operations and additionally provides access to in-memory objects to facilitate more novel use cases. These options allow users to integrate the package into pre-existing bash and Python scripts, in addition to providing some handy tools for use in day-to-day work with NWP systems. The ``uwtools`` Rocoto tool has been incorporated into the Land DA System to generate and validate the Rocoto XML file used to run the workflow tasks. More details about UW tools can be found in the `uwtools GitHub repository <https://github.com/ufs-community/uwtools>`_ and in the :uw:`UW Documentation <>`.
