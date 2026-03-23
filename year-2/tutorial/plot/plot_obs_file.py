#!/usr/bin/env python3

###################################################################### CHJ #####
## Name		  : plot_obs_file.py
## Usage	  : Plot observation data files
## NOAA/EPIC
## History ===============================
## V000: 2024/12/03: Chan-Hoo Jeon : Preliminary version
## V001: 2025/04/17: Chan-Hoo Jeon : Add IMS option
## V002: 2025/11/13: Chan-Hoo Jeon : Add SOCA option
## V003: 2026/02/06: Chan-Hoo Jeon : Add ATM option
###################################################################### CHJ #####

import os, sys
import logging
import yaml
import numpy as np
import netCDF4 as nc
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


# Main part (will be called at the end) ============================= CHJ =====
def main():
    global obs_dir, diags_dir, diags_obs_plot
    yaml_file="plot_obs_file.yaml"
    with open(yaml_file, 'r') as f:
        yaml_data=yaml.load(f, Loader=yaml.FullLoader)
    f.close()

    work_dir = yaml_data['work_dir']
    obs_dir = yaml_data['obs_dir']
    cartopy_ne_path = yaml_data['cartopy_ne_path']
    diags_dir = yaml_data['diags_dir']
    diags_obs_plot = yaml_data['diags_obs_plot']
    TYPE_ANAL_FCST = yaml_data['TYPE_ANAL_FCST']
    JEDI_TYPE_FV3 = yaml_data['JEDI_TYPE_FV3']
    JEDI_TYPE_SOCA = yaml_data['JEDI_TYPE_SOCA']
    OBS_ATM_AMV_ABI_GOES_16 = yaml_data['OBS_ATM_AMV_ABI_GOES_16']
    OBS_ATM_ASCAT_W = yaml_data['OBS_ATM_ASCAT_W']
    OBS_ATM_ATMS_N20= yaml_data['OBS_ATM_ATMS_N20']
    OBS_ATM_CONVENTIONAL_PS = yaml_data['OBS_ATM_CONVENTIONAL_PS']
    OBS_ATM_GNSSRO_COSMIC2 = yaml_data['OBS_ATM_GNSSRO_COSMIC2']
    OBS_ATM_OZONE_OMPSNP_NPP = yaml_data['OBS_ATM_OZONE_OMPSNP_NPP']
    OBS_ATM_OZONE_OMPSTC_NPP = yaml_data['OBS_ATM_OZONE_OMPSTC_NPP']
    OBS_SNOW_GHCN = yaml_data['OBS_SNOW_GHCN']
    OBS_SNOW_IMS = yaml_data['OBS_SNOW_IMS']
    OBS_SWC_SMAP = yaml_data['OBS_SWC_SMAP']
    OBS_SWC_SMOPS = yaml_data['OBS_SWC_SMOPS']
    obs_prefix = yaml_data['obs_prefix']
    PDY = yaml_data['PDY']
    cyc = yaml_data['cyc']
    PY_LOG_LEVEL = yaml_data['PY_LOG_LEVEL']
 
    # Set logging config
    log_level_str = PY_LOG_LEVEL.upper()
    try:
        log_level = getattr(logging, log_level_str)
    except AttributeError:
        log_level_str = "INFO"
        log_level = logging.INFO
        print(f''' WARNING: Invalid log level "{PY_LOG_LEVEL.upper()}", set to INFO.''')
    print(f''' Python Log Level= str: {log_level_str}, attr: {log_level}''')
    logging.basicConfig(format='%(levelname)s::%(pathname)s::L%(lineno)d::%(message)s', level=log_level)

    logging.info(f''' YAML Data: {yaml_data}''')

    # Set the path to Natural Earth dataset
    cartopy.config['data_dir']=cartopy_ne_path

    # Plot AMV_ABI_GOES16
    if OBS_ATM_AMV_ABI_GOES_16 == "YES":
        obs_plot("goes16_e",PDY,cyc,work_dir,obs_prefix,"satwnd.abi_goes-16","satwnd.abi_goes-16")
        obs_plot("goes16_n",PDY,cyc,work_dir,obs_prefix,"satwnd.abi_goes-16","satwnd.abi_goes-16")
    # Plot ASCAT_W
    if OBS_ATM_ASCAT_W == "YES":
        obs_plot("ascat_e",PDY,cyc,work_dir,obs_prefix,"scatwnd.ascat_metop-b","scatwnd.ascat_metop-b")
        obs_plot("ascat_n",PDY,cyc,work_dir,obs_prefix,"scatwnd.ascat_metop-b","scatwnd.ascat_metop-b")
    # Plot ATMS_N20
    if OBS_ATM_ATMS_N20 == "YES":
        obs_plot("atms_n20",PDY,cyc,work_dir,obs_prefix,"atms_n20","atms_n20")
    # Plot CONVENTIONAL_PS
    if OBS_ATM_CONVENTIONAL_PS == "YES":
        obs_plot("conventional_ps",PDY,cyc,work_dir,obs_prefix,"conventional_ps","conventional_ps")
    # Plot GNSSRO_COSMIC2
    if OBS_ATM_GNSSRO_COSMIC2== "YES":
        obs_plot("gnssro_cosmic2",PDY,cyc,work_dir,obs_prefix,"gnssro_cosmic2","gnssro_cosmic2")
    # Plot OZONE_OMPSNP_NPP
    if OBS_ATM_OZONE_OMPSNP_NPP== "YES":
        obs_plot("ompsnp_npp",PDY,cyc,work_dir,obs_prefix,"ozone.ompsnp_npp","ozone.ompsnp_npp")
    # Plot OZONE_OMPSTC_NPP
    if OBS_ATM_OZONE_OMPSTC_NPP== "YES":
        obs_plot("ompstc_npp",PDY,cyc,work_dir,obs_prefix,"ozone.ompstc_npp","ozone.ompstc_npp")
    # Plot GHCN
    if OBS_SNOW_GHCN == "YES":
        obs_plot("ghcn",PDY,cyc,work_dir,obs_prefix,"ghcn_snow","ghcn_snow")
    # Plot IMS
    if OBS_SNOW_IMS == "YES":
        obs_plot("ims",PDY,cyc,work_dir,obs_prefix,"ims_snow.tm00","ims_snow")
    # Plot SMAP
    if OBS_SWC_SMAP == "YES":
        obs_plot("smap",PDY,cyc,work_dir,obs_prefix,"smap_combined","smap_soil_moisture")
    # Plot SMOPS
    if OBS_SWC_SMOPS == "YES":
        obs_plot("smops",PDY,cyc,work_dir,obs_prefix,"smops","smops_soil_moisture")
    # Plot SOCA
    if JEDI_TYPE_SOCA == "YES":
        if TYPE_ANAL_FCST == "ctest":
            obs_plot("soca_sst",PDY,cyc,work_dir,obs_prefix,"sst","SeaSurfaceTemp")
            obs_plot("soca_sss",PDY,cyc,work_dir,obs_prefix,"sss","SeaSurfaceSalinity")
            obs_plot("soca_adt",PDY,cyc,work_dir,obs_prefix,"adt","ADT")
            obs_plot("soca_prof_t",PDY,cyc,work_dir,obs_prefix,"prof","InsituTemperature")
            obs_plot("soca_prof_s",PDY,cyc,work_dir,obs_prefix,"prof","InsituSalinity")
            obs_plot("soca_icec",PDY,cyc,work_dir,obs_prefix,"icec","SeaIceFraction")
        else:
            obs_plot("soca_adt",PDY,cyc,work_dir,obs_prefix,"adt_ssh","ADT")
            obs_plot("soca_sst",PDY,cyc,work_dir,obs_prefix,"sst_satellite","SeaSurfaceTemp")
            obs_plot("soca_sss",PDY,cyc,work_dir,obs_prefix,"sss_salinity","SeaSurfaceSalinity")
            obs_plot("soca_prof_t",PDY,cyc,work_dir,obs_prefix,"rtofs_prof_waterTemperature","InsituTemperature")
            obs_plot("soca_prof_s",PDY,cyc,work_dir,obs_prefix,"rtofs_prof_salinity","InsituSalinity")
    # Plot FV3-JEDI
    if JEDI_TYPE_FV3 == "YES":
        if TYPE_ANAL_FCST == "ctest":
            obs_plot("fv3_geos",PDY,cyc,work_dir,obs_prefix,"tropomi_no2","tropomi_no2")


# obs plot =============================================== CHJ =====
def obs_plot(obs_type,PDY,cyc,work_dir,fn_prefix,fn_suffix,fn_diag):

    # open the data files
    ## Original observation file
    fn_input = f'''{fn_prefix}.{fn_suffix}.nc'''
    logging.info(f''' ===== INPUT:: {obs_type}:: '{fn_input}' ================================''')
    fpath = os.path.join(obs_dir,fn_input)
    try: mdat = nc.Dataset(fpath)
    except: raise Exception('Could NOT find the file',fpath)
    logging.debug(" MetaData(orig):", mdat.groups['MetaData'])
    logging.debug(" ObsValue(orig):", mdat.groups['ObsValue'])
    lon = mdat.groups['MetaData'].variables['longitude'][:]
    lat = mdat.groups['MetaData'].variables['latitude'][:]

    ## Observation data in H(x) output file
    if diags_obs_plot == "YES":
        diags_fn = f'''diag.{fn_diag}_{PDY}{cyc}.nc'''
        diags_fp = os.path.join(diags_dir,diags_fn)
        try: odat = nc.Dataset(diags_fp)
        except: raise Exception('Could NOT find the file',diags_fp)
        logging.debug(" MetaData(hofx):", odat.groups['MetaData'])
        logging.debug(" ObsValue(hofx):", odat.groups['ObsValue'])
        olon = odat.groups['MetaData'].variables['longitude'][:]
        olat = odat.groups['MetaData'].variables['latitude'][:]

    # Variables
    #vars_out=["ObsValue", "ObsError", "PreQC"]
    vars_out=["ObsValue"]

    extent=[]
    if obs_type == "fv3_geos":
        # for CONUS
        extent=[-125,-66,23,53]
    else:
        # for Northern Hemisphere (default)
        extent=[-179,179,0,82.5]
    logging.info(f''' Map extent= {extent}''')

    #c_lon=np.mean(extent[:2])
    c_lon=-77.0369 # D.C.
    logging.info(f''' c_lon= {c_lon}''')

    for svar in vars_out:
        svar_plot(svar,mdat,lon,lat,c_lon,extent,obs_type,PDY,work_dir,'orig')
        if diags_obs_plot == "YES":
            svar_plot(svar,odat,olon,olat,c_lon,extent,obs_type,PDY,work_dir,'hofx')


# Variable plot =============================================== CHJ =====
def svar_plot(svar,mdat,lon,lat,c_lon,extent,obs_type,PDY,work_dir,dat_txt):

    logging.info(f''' ===== {svar} ({dat_txt}) ==========================================''')

    cs_cmap='gist_ncar_r'
    lb_ext='neither'
    tick_ln=1.5
    tick_wd=0.45
    tlb_sz=3
    n_rnd=2
    cmap_range='fixed'
    scat_sz=0.2

    # Extract data array
    if obs_type == "smap" or obs_type == "smops":
        gvar = "soilMoistureVolumetric"
        pvar = "Soil Moisture"
    elif obs_type == "ghcn" or obs_type == "ims":
        gvar = "totalSnowDepth"
        pvar = "Snow Depth"
    elif obs_type == "soca_sst":
        gvar = "seaSurfaceTemperature"
        pvar = "Sea Surface Temperature"
    elif obs_type == "soca_sss":
        gvar = "seaSurfaceSalinity"
        pvar = "Sea Surface Salinity"
    elif obs_type == "soca_adt":
        gvar = "absoluteDynamicTopography"
        pvar = "Absolute Dynamic Topography"
    elif obs_type == "soca_icec":
        gvar = "seaIceFraction"
        pvar = "Sea Ice Fraction"
    elif obs_type == "soca_prof_t":
        gvar = "waterTemperature"
        pvar = "Insitu Temperature"
    elif obs_type == "soca_prof_s":
        gvar = "salinity"
        pvar = "Insitu Salinity"
    elif obs_type == "fv3_geos":
        gvar = "nitrogendioxideColumn"
        pvar = "Nitrogen dioxide (NO2)"
    elif obs_type == "goes16_e":
        gvar = "windEastward"
        pvar = "Eastward wind component (m/s)"
    elif obs_type == "goes16_n":
        gvar = "windNorthward"
        pvar = "Northward wind component (m/s)"
    elif obs_type == "ascat_e":
        gvar = "windEastward"
        pvar = "Eastward wind component at 10m (m/s)"
    elif obs_type == "ascat_n":
        gvar = "windNorthward"
        pvar = "Northward wind component at 10m (m/s)"
    elif obs_type == "atms_n20":
        gvar = "brightnessTemperature"
        pvar = "3x3 averaged brightness temperature (K)"
    elif obs_type == "conventional_ps":
        gvar = "stationPressure"
        pvar = "Station Pressue Quality Marker"
    elif obs_type == "gnssro_cosmic2":
        gvar = "bendingAngle"
        pvar = "Bending angle (radians)"
    elif obs_type == "ompsnp_npp":
        gvar = "ozoneLayer"
        pvar = "Layer Ozone (DU)"
    elif obs_type == "ompstc_npp":
        gvar = "ozoneTotal"
        pvar = "Total column ozone (DU)"
    else:
        gvar = svar
        pvar = svar

    lon_len = len(lon)
    obs_type_upper = obs_type.upper()
    if obs_type == "atms_n20":
        # channel number (total=22)
        ich = 1
        logging.info(f''' ATMS_N20: Channel number = {ich}''')
        sfld = mdat.groups[svar].variables[gvar][:,ich-1]
        out_title_fld = f'''Obs({dat_txt},N={lon_len})::{obs_type_upper}::{PDY}::{gvar}::CH{ich}'''
        out_fn = f'''obs_{dat_txt}_{obs_type}_{PDY}_{gvar}_ch{ich}'''
    else:
        sfld = mdat.groups[svar].variables[gvar][:]
        out_title_fld = f'''Obs({dat_txt},N={lon_len})::{obs_type_upper}::{PDY}::{gvar}'''
        out_fn = f'''obs_{dat_txt}_{obs_type}_{PDY}_{gvar}'''

    # Check array size
    lat_len = len(lat)
    sfld_len = len(sfld)
    logging.info(f''' length of lon = {lon_len}''')
    logging.info(f''' length of lat = {lat_len}''')
    logging.info(f''' lenght of sfld = {sfld_len}''')
    if lon_len != lat_len or lon_len != sfld_len or lat_len != sfld_len:
        sys.exit('FATAL ERROR: array size mismatched !!!')


    # Max and Min of the field
    fmax = np.max(sfld)
    fmin = np.min(sfld)
    logging.info(f''' Max of {pvar}= {fmax}''')
    logging.info(f''' Min of {pvar}= {fmin}''')

    # Make the colormap range symmetry
    logging.info(f''' cmap range= {cmap_range}''')
    if cmap_range=='symmetry':
        tmp_cmp=max(abs(fmax),abs(fmin))
        cs_min=round(-tmp_cmp,n_rnd)
        cs_max=round(tmp_cmp,n_rnd)
    elif cmap_range=='round':
        cs_min=round(fmin,n_rnd)
        cs_max=round(fmax,n_rnd)
    elif cmap_range=='real':
        cs_min=fmin
        cs_max=fmax
    elif cmap_range=='fixed':
        cs_min=0
        if obs_type == 'ims':
            cs_max=100.0
        elif obs_type == 'ghcn':
            cs_max=1000.0
        elif obs_type == 'smap' or obs_type == 'smops':
            cs_max=1.0
            cs_min=0.0
        elif obs_type == 'soca_sst' or obs_type == 'soca_prof_t':
            cs_max = 35
            cs_min = -5
        elif obs_type == 'soca_sss' or obs_type == 'soca_prof_s':
            cs_max = 38
            cs_min = 30
        elif obs_type == 'soca_adt':
            cs_max = 1.4
            cs_min = -1.4
            cs_cmap = 'turbo'
        elif obs_type == 'soca_icec':
            cs_max = 1
            cs_min = 0
        elif obs_type == 'fv3_geos':
            cs_max = 3e-05
            cs_min = 0
        elif obs_type == 'goes16_e' or obs_type == 'goes16_n':
            cs_max = 60
            cs_min = -60
            cs_cmap = 'turbo'
        elif obs_type == 'ascat_e' or obs_type == 'ascat_n':
            cs_max = 20
            cs_min = -20
            cs_cmap = 'turbo'
        elif obs_type == 'atms_n20':
            cs_max = 300.0
            cs_min = 100.0
        elif obs_type == 'conventional_ps':
            cs_max = 105000.0
            cs_min = 75000.0
            cs_cmap = 'turbo'
        elif obs_type == 'gnssro_cosmic2':
            cs_max = 0.03
            cs_min = 0.0
        elif obs_type == 'ompsnp_npp':
            cs_max = 600.0
            cs_min = 200.0
            cs_cmap = 'turbo'
        elif obs_type == 'ompstc_npp':
            cs_max = 600.0
            cs_min = 200.0
            cs_cmap = 'turbo'
        else:
            cs_max=300.0
    else:
        sys.exit('FATAL ERROR: wrong colormap-range flag !!!')

    logging.info(f''' cs_max= {cs_max}''')
    logging.info(f''' cs_min= {cs_min}''')

    # Plot field
    fig,ax=plt.subplots(1,1,subplot_kw=dict(projection=ccrs.Robinson(c_lon)))
    if obs_type == "ghcn" or obs_type == "fv3_geos":
        ax.set_extent(extent, ccrs.PlateCarree())
    else:
        ax.set_global()

    # Call background plot
    back_plot(ax)
    ax.set_title(out_title_fld,fontsize=8)
    cs=ax.scatter(lon,lat,transform=ccrs.PlateCarree(),c=sfld,cmap=cs_cmap,
                  vmin=cs_min,vmax=cs_max,s=scat_sz)
    divider=make_axes_locatable(ax)
    ax_cb=divider.new_horizontal(size="3%",pad=0.1,axes_class=plt.Axes)
    fig.add_axes(ax_cb)
    cbar=plt.colorbar(cs,cax=ax_cb,extend=lb_ext)
    cbar.ax.tick_params(labelsize=7)
    cbar.set_label(pvar,fontsize=7)

    # Output figure
    ndpi=300
    out_file(work_dir,out_fn,ndpi)


# Background plot ==================================================== CHJ =====
def back_plot(ax):
    # Resolution of background natural earth data ('50m' or '110m')
    back_res='50m'

    fline_wd=0.5  # line width
    falpha=0.7 # transparency

    # natural_earth
    land=cfeature.NaturalEarthFeature('physical','land',back_res,
                      edgecolor='face',facecolor=cfeature.COLORS['land'],
                      alpha=falpha)
    lakes=cfeature.NaturalEarthFeature('physical','lakes',back_res,
                      edgecolor='blue',facecolor='none',
                      linewidth=fline_wd,alpha=falpha)
    coastline=cfeature.NaturalEarthFeature('physical','coastline',
                      back_res,edgecolor='black',facecolor='none',
                      linewidth=fline_wd,alpha=falpha)
    states=cfeature.NaturalEarthFeature('cultural','admin_1_states_provinces',
                      back_res,edgecolor='green',facecolor='none',
                      linewidth=fline_wd,linestyle=':',alpha=falpha)
    borders=cfeature.NaturalEarthFeature('cultural','admin_0_countries',
                      back_res,edgecolor='red',facecolor='none',
                      linewidth=fline_wd,alpha=falpha)

#    ax.add_feature(land)
#    ax.add_feature(lakes)
#    ax.add_feature(states)
#    ax.add_feature(borders)
    ax.add_feature(coastline)


# Output file ======================================================= CHJ =====
def out_file(work_dir,out_file,ndpi):
    # Output figure
    fp_out=os.path.join(work_dir,out_file)
    plt.savefig(fp_out+'.png',dpi=ndpi,bbox_inches='tight')
    plt.close('all')


# Main call ========================================================= CHJ =====
if __name__=='__main__':
    main()

