.. _Glossary:

**********
Glossary
**********

.. glossary::

   3D-Var
      Three-Dimensional Variational data assimilation

   ATM
      The Weather Model configuration that runs only the standalone atmospheric model. 

   ATML
      The ATML configuration of the Land DA System uses the Noah-MP :term:`land component` from the UFS :term:`Weather Model` with an active :term:`FV3` atmospheric component (`fv3atm <https://github.com/NOAA-EMC/fv3atm>`_). 

   CCPP
      The `Common Community Physics Package <https://dtcenter.org/community-code/common-community-physics-package-ccpp>`_ is a forecast-model agnostic, vetted collection of code containing atmospheric physical parameterizations and suites of parameterizations for use in Numerical Weather Prediction (NWP) along with a framework that connects the physics to the host forecast model.

   CDEPS
      The `Community Data Models for Earth Predictive Systems <https://github.com/NOAA-EMC/CDEPS/>`_ repository (CDEPS) contains a set of :term:`NUOPC`-compliant data components and :term:`ESMF`-based "stream" code that selectively removes feedback in coupled model systems. In essence, CDEPS handles the static Data Atmosphere (:term:`DATM`) integration with dynamic coupled model components (e.g., :term:`MOM6`). The CDEPS data models perform the basic function of reading external data files, modifying those data, and then sending the data back to the :term:`CMEPS` mediator. The fields sent to the :term:`mediator` are the same as those that would be sent by an active component. This takes advantage of the fact that the mediator and other CMEPS-compliant model components have no fundamental knowledge of whether another component is fully active or just a data component. More information about DATM is available in the CDEPS `Documentation <https://escomp.github.io/CDEPS/versions/master/html/index.html>`_.

   CESM
      The `Community Earth System Model <https://www.cesm.ucar.edu/>`_ (CESM) is a fully-coupled global climate model developed at the National Center for Atmospheric Research (:term:`NCAR`) in collaboration with colleagues in the research community. 

   CMEPS
      The `Community Mediator for Earth Prediction Systems <https://github.com/NOAA-EMC/CMEPS>`_ (CMEPS) is a :term:`NUOPC`-compliant :term:`mediator` used for coupling Earth system model components. It is currently being used in NCAR's Community Earth System Model (:term:`CESM`) and NOAA's subseasonal-to-seasonal (S2S) coupled system. More information is available in the `CMEPS Documentation <https://escomp.github.io/CMEPS/versions/master/html/index.html>`_.

   coldstart
   cold start
      A coldstart forecast initializes a model using data from a different source (e.g., climatology data, forecast data from a different model, analysis files) to "spin up," or start, the forecast. 
   
   container
      `Docker <https://www.docker.com/resources/what-container>`_ describes a container as "a standard unit of software that packages up code and all its dependencies so the application runs quickly and reliably from one computing environment to another."

   cron
   cron job
   crontab
   cron table
      Cron is a job scheduler accessed through the command-line on UNIX-like operating systems. It is useful for automating tasks such as regression testing. Cron periodically checks a cron table (aka crontab) to see if any tasks are are ready to execute. If so, it runs them. 

   cycle
      An hour of the day on which a forecast is started. In the Land DA System, it usually follows YYYYMMDD-HHmmss format. 

   data assimilation
   DA
      One of the major sources of error in weather and climate forecasts is uncertainty related to the initial conditions that are used to generate future predictions. Even the most precise instruments have a small range of unavoidable measurement error, which means that tiny measurement errors (e.g., related to atmospheric conditions and instrument location) can compound over time. These small differences result in very similar forecasts in the short term (i.e., minutes, hours), but they cause widely divergent forecasts in the long term. Errors in weather and climate forecasts can also arise because models are imperfect representations of reality. Data assimilation systems seek to mitigate these problems by combining the most timely observational data with a "first guess" of the atmospheric state (usually a previous forecast) and other sources of data to provide a "best guess" analysis of the atmospheric state to start a weather or climate simulation. When combined with an "ensemble" of model runs (many forecasts with slightly different conditions), data assimilation helps predict a range of possible atmospheric states, giving an overall measure of uncertainty in a given forecast. 
   
   DATM
      DATM is the *Data Atmosphere* component of :term:`CDEPS`. It uses static atmospheric forcing files (derived from observations or previous atmospheric model runs) instead of output from an active atmospheric model. This reduces the complexity and computational cost associated with coupling to an active atmospheric model. The *Data Atmosphere* component is particularly useful when employing computationally intensive Data Assimilation (DA) techniques to update ocean and/or sea ice fields in a coupled model. In general, use of DATM in place of :term:`ATM` can be appropriate when users are running a coupled model and only want certain components of the model to be active. More information about DATM is available in the `CDEPS Documentation <https://escomp.github.io/CDEPS/versions/master/html/datm.html>`_.

   dycore
   dynamical core
      Global atmospheric model based on fluid dynamics principles, including Euler’s equations of motion.

   ERA5
      The ECMWF Reanalysis v5 (`ERA5 <https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5>`_) dataset "is the fifth generation ECMWF atmospheric reanalysis of the global climate covering the period from January 1940 to present." It "provides hourly estimates of a large number of atmospheric, land and oceanic climate variables."

   ESMF
      `Earth System Modeling Framework <https://earthsystemmodeling.org/docs/release/latest/ESMF_usrdoc/>`_. The ESMF defines itself as "a suite of software tools for developing high-performance, multi-component Earth science modeling applications." It is a community-developed software infrastructure for building and coupling models. 

   ex-scripts
      Scripting layer (contained in ``land-DA_workflow/jobs/``) that should be called by a :term:`J-job <J-jobs>` for each workflow component to run a specific task or sub-task in the workflow. The different scripting layers are described in detail in the :nco:`NCO Implementation Standards document <ImplementationStandards.v11.0.0.pdf>`.

   FMS
      The Flexible Modeling System (`FMS <https://www.gfdl.noaa.gov/fms/>`_) is a software framework for supporting the efficient
      development, construction, execution, and scientific interpretation of atmospheric, 
      oceanic, and climate system models.

   forcing data
      In coupled mode, data that are generated by one component of a model can be fed into another component to provide required input describing the state of the Earth system. When models are run in offline, or "uncoupled" mode, the model does not receive this input from another active component, so "forcing" files are provided. These files may consist of observational data or data gathered when running other components separately, and they contain values for the required input fields. 

   FV3
      The Finite-Volume Cubed-Sphere dynamical core (dycore). Developed at NOAA’s `Geophysical Fluid Dynamics Laboratory <https://www.gfdl.noaa.gov/fv3/>`__ (GFDL), it is a scalable and flexible dycore capable of both hydrostatic and non-hydrostatic atmospheric simulations. It is the dycore used in the UFS Weather Model.

   GDAS
      The Global Data Assimilation System (`GDAS <https://catalog.data.gov/dataset/global-data-assimilation-system-gdas2>`_) is "the system used by the Global Forecast System (:term:`GFS`) model to place observations into a gridded model space for the purpose of starting, or initializing, weather forecasts with observed data."

   GFS
      The Global Forecast System (`GFS <https://www.ncei.noaa.gov/products/weather-climate-models/global-forecast>`_) is an :term:`NCEP` model that "generates data for dozens of atmospheric and land-soil variables." It couples atmosphere, ocean, land/soil, and sea ice models to accurately depict weather conditions.

   GHCN 
      The Global Historical Climatology Network (`GHCN <https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-daily>`_) is "an integrated database of daily climate summaries from land surface stations across the globe."" 

   GSWP3
      The Global Soil Wetness Project Phase 3 dataset is a century-long comprehensive set of data documenting several variables for hydro-energy-eco systems. 

   HPC
      High-Performance Computing.

   IMS 
      The `Interactive Multisensor Snow and Ice Mapping System <https://usicecenter.gov/Products/ImsHome>`_ (IMS) is "an operational software package used to demarcate the presence of snow and ice across the entire northern hemisphere."

   IODA
      The :term:`JEDI` Interface for Observation Data Access (:jedi:`IODA <inside/jedi-components/ioda/index.html>`) provides observation formatting and processing tools for data assimilation applications.  
      .. COMMENT: Add! https://github.com/jcsda/ioda

   J-jobs
      Scripts (contained in ``land-DA_workflow/jobs/``) that should be directly called for each workflow component (either on the command line or by the workflow manager) to run a specific task in the workflow. The different scripting layers are described in detail in the :nco:`NCO Implementation Standards document <ImplementationStandards.v11.0.0.pdf>`.

   JCB
   JEDI Configuration Builder
      The JEDI Configuration Builder (JCB) is a python package used to assemble information on :term:`JEDI` algorithms (e.g., letkf, 3dvar) and data assimilation types (e.g., snow, marine, atmosphere) into one convenient YAML file for use in data assimilation applications. 
      .. COMMENT: Add/revise def! 

   JEDI
      The Joint Effort for Data assimilation Integration (`JEDI <https://www.jcsda.org/jcsda-project-jedi>`_) is a unified and versatile data assimilation (DA) system for Earth System Prediction. It aims to enable efficient research and accelerated transition from research to operations by providing a framework that takes into account all components of the Earth system in a consistent manner. The JEDI software package can run on a variety of platforms and for a variety of purposes, and it is designed to readily accommodate new atmospheric and oceanic models and new observation systems. The `JEDI User's Guide <https://jointcenterforsatellitedataassimilation-jedi-docs.readthedocs-hosted.com/en/latest/>`_ contains extensive information on the software. 

      JEDI is developed and distributed by the `Joint Center for Satellite Data Assimilation <https://www.jcsda.org/>`_, a multi-agency research center hosted by the University Corporation for Atmospheric Research (`UCAR <https://www.ucar.edu/>`_). JCSDA is dedicated to improving and accelerating the quantitative use of research and operational satellite data in weather, ocean, climate, and environmental analysis and prediction systems.

   jedi-bundle
      :term:`JCSDA`'s `jedi-bundle <https://github.com/JCSDA/jedi-bundle>`_ repository provides an integrated Earth System data assimilation capability. It combines a variety of :term:`JEDI` components, including :term:`OOPS`, :term:`IODA`, and :term:`UFO`. 

   LND
      The LND experiment configuration uses the :term:`land component` with a :term:`DATM` component. 

   land component
      The Noah Multi-Physics (Noah-MP) land surface model (LSM) is an open-source, community-developed LSM that has been incorporated into the UFS Weather Model (WM). It is the UFS WM's land component. 

   LETKF
      Local Ensemble Transform Kalman Filter (LETKF) data assimilation

   LETKF-OI
      Local Ensemble Transform Kalman Filter-Optimal Interpolation (see :cite:t:`HuntEtAl2007`, 2007).

   Mediator
      A mediator, sometimes called a coupler, is a software component that includes code for representing component interactions. Typical operations include merging data fields, ensuring consistent treatment of coastlines, computing fluxes, and temporal averaging.

   MOM
   MOM6
   Modular Ocean Model
      MOM6 is the latest generation of the Modular Ocean Model. It is numerical model code for simulating the ocean general circulation. MOM6 was originally developed by the `Geophysical Fluid Dynamics Laboratory <https://www.gfdl.noaa.gov/mom-ocean-model/>`__. Currently, `MOM6 code <https://github.com/mom-ocean/MOM6>`_ and an `extensive suite of test cases <https://github.com/NOAA-GFDL/MOM6-examples/wiki>`_ are available under an open-development software framework. Although there are many public forks of MOM6, the `NOAA EMC fork <https://github.com/NOAA-EMC/MOM6>`_ is used in the UFS Weather Model. 

   MPI
      MPI stands for Message Passing Interface. An MPI is a standardized communication system used in parallel programming. It establishes portable and efficient syntax for the exchange of messages and data between multiple processors that are used by a single computer program. An MPI is required for high-performance computing (HPC) systems.

   NCAR
      The `National Center for Atmospheric Research <https://ncar.ucar.edu/>`_. 

   netCDF
      NetCDF (`Network Common Data Form <https://www.unidata.ucar.edu/software/netcdf/>`_) is a file format and community standard for storing multidimensional scientific data. It includes a set of software libraries and machine-independent data formats that support the creation, access, and sharing of array-oriented scientific data.

   NCEP
      National Centers for Environmental Prediction (NCEP) is an arm of the National Weather Service consisting of nine centers. More information can be found at https://www.weather.gov/ncep/.
   
   NCO
      :term:`NCEP` Central Operations. Visit the `NCO website <https://www.nco.ncep.noaa.gov/>`_ for more information.

   NUOPC
   National Unified Operational Prediction Capability
      The `National Unified Operational Prediction Capability <https://earthsystemmodeling.org/nuopc/>`_ is a consortium of Navy, NOAA, and Air Force modelers and their research partners. It aims to advance the weather modeling systems used by meteorologists, mission planners, and decision makers. NUOPC partners are working toward a common model architecture --- a standard way of building models --- in order to make it easier to collaboratively build modeling systems.

   Noah-MP
      
      .. COMMENT: Add!

   NUOPC Layer
      The :term:`NUOPC` Layer "defines conventions and a set of generic components for building coupled models using the Earth System Modeling Framework (:term:`ESMF`)." 
      NUOPC applications are built on four generic components: driver, model, mediator, and connector. For more information, visit the `NUOPC website <https://earthsystemmodeling.org/nuopc/>`_.

   NUOPC Cap
   NUOPC Model Cap
      A NUOPC "cap" is an interface between a given model component and the rest of a coupled model system. It is a small software layer that sits on top of the component model, making calls into it. 

   NWP
      Numerical Weather Prediction (NWP) takes current observations of weather and processes them with computer models to forecast the future state of the weather. 

   OOPS
      The :term:`JEDI` Object-Oriented Prediction System (:jedi:`OOPS <inside/jedi-components/oops/index.html>`) includes data assimilation algorithms for use in data assimilation applications.  
      .. COMMENT: Add! https://github.com/jcsda/oops

   RDHPCS
      `Research and Development High-Performance Computing Systems <https://docs.rdhpcs.noaa.gov/systems/index.html>`_. 

   SFCSNO
      Global Telecommunication System data available from :term:`GDAS`/:term:`GFS`. 

   Skylab
      `JEDI Skylab <https://www.jcsda.org/jediskylab>`_ is the name for roll-up releases of :term:`JCSDA`'s `jedi-bundle <https://github.com/JCSDA/jedi-bundle>`_ repository. 
      This software provides an integrated Earth System Data Assimilation capability. JCSDA has tested Skylab capabilities internally via the SkyLab testbed for the following components: atmosphere, land/snow, ocean, sea-ice, aerosols, and atmospheric composition. However, JCSDA plans to stop releasing ``jedi-bundle`` and instead encourage users and developers to move to the ``develop`` branch, which will contain the latest updates. 

   Spack
      `Spack <https://spack.readthedocs.io/en/latest/>`_ is a package management tool designed to support multiple versions and configurations of software on a wide variety of platforms and environments. It was designed for large supercomputing centers where many users and application teams share common installations of software on clusters with exotic architectures. 

   spack-stack
      The `spack-stack <https://github.com/JCSDA/spack-stack>`_ is a collaborative effort between the NOAA Environmental Modeling Center (EMC), the UCAR Joint Center for Satellite Data Assimilation (JCSDA), and the Earth Prediction Innovation Center (EPIC). *spack-stack* is a repository that provides a :term:`Spack`-based method for building the software stack required for numerical weather prediction (NWP) tools such as the :ufs:`Unified Forecast System (UFS) <>` and the :jedi:`Joint Effort for Data assimilation Integration (JEDI) <>` framework. *spack-stack* uses the Spack package manager along with custom Spack configuration files and Python scripts to simplify installation of the libraries required to run various applications. The *spack-stack* can be installed on a range of platforms and comes pre-configured for many systems. Users can install the necessary packages for a particular application and later add the missing packages for another application without having to rebuild the entire stack.

   UFO
      The :term:`JEDI` Unified Forward Operator (:jedi:`UFO <inside/jedi-components/ufo/index.html>`) is used to compare model forecasts and observations in data assimilation applications. 
      .. COMMENT: Add! https://github.com/jcsda/ufo.git

   UFS
      The Unified Forecast System (UFS) is a community-based, coupled, comprehensive Earth modeling system consisting of several applications (apps). These apps span regional to global domains and sub-hourly to seasonal time scales. The UFS is designed to support the :term:`Weather Enterprise` and to be the source system for NOAA's operational numerical weather prediction applications. For more information, visit the :ufs:`UFS Portal <>`.

   Umbrella repository
      A repository that houses external code, or “externals,” from additional repositories.

   warmstart
   warm start
      A warmstart forecast uses "saved fields from a recent forecast of the same model" (often provided via RESTART files) to populate certain variables (https://www.oc.nps.edu/nom/modeling/initial.html). This is in contrast to a :term:`coldstart`. 

   Weather Enterprise
      Individuals and organizations from public, private, and academic sectors that contribute to the research, development, and production of weather forecast products; primary consumers of these weather forecast products.

   Weather Model
   WM
      A prognostic model that can be used for short- and medium-range research and operational forecasts. It can be an atmosphere-only model or an atmospheric model coupled with one or more additional components, such as a wave or ocean model. The SRW App uses the `UFS Weather Model <https://github.com/ufs-community/ufs-weather-model/wiki>`_.