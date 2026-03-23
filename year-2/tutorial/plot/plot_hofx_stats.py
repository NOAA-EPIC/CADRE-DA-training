#!/usr/bin/env python3

import os
import sys
import logging
import yaml
import numpy as np
import netCDF4
import matplotlib.pyplot as plt
from scipy.stats import norm
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr
import matplotlib.ticker
import matplotlib as mpl
from matplotlib.colors import ListedColormap

def get_obs_stats(fname, svar_long):

    logging.info(f''' === File Name: {fname}''')
    f=netCDF4.Dataset(fname)
    if svar_long == "brightnessTemperature":
        # Channel number
        ich = 1
        ichm1 = ich - 1
        obs=f.groups['ObsValue'].variables[svar_long][:,ichm1]
        omb=f.groups['ombg'].variables[svar_long][:,ichm1]
    else:
        obs=f.groups['ObsValue'].variables[svar_long][:]
        omb=f.groups['ombg'].variables[svar_long][:]
    logging.debug("ObsValue:",obs)
    logging.debug("OMBG:",omb)
    lat=f.groups['MetaData'].variables['latitude'][:]
    lon=f.groups['MetaData'].variables['longitude'][:]

    numpt_omb=len(omb)
    numpt_obs=len(obs)
    logging.info(f'''Number of points (raw): {numpt_omb}, {numpt_obs}''')
    if numpt_omb == 0 or numpt_obs == 0:
        logging.warning(f''' Number of OMB or OBS is zero !!!''')
        sys.exit(0)

    obs = [x for x, y in zip(obs, omb) if y>-5000 and y<5000]
    lat = [x for x, y in zip(lat, omb) if y>-5000 and y<5000]
    lon = [x for x, y in zip(lon, omb) if y>-5000 and y<5000]
    omb = [x for x in omb if x>-5000 and x<5000]
    numpt_omb=len(omb)
    numpt_obs=len(obs)
    logging.info(f'''Number of points (excluding zeros): {numpt_omb}, {numpt_obs}''')
    max_omb=np.max(omb)
    min_omb=np.min(omb)
    max_obs=np.max(obs)
    min_obs=np.min(obs)
    logging.info(f'''OMB max/min: {max_omb}, {min_omb}''')
    logging.info(f'''OBS max/min: {max_obs}, {min_obs}''')

    return omb,lat,lon


def plot_scatter(omb,svar,hofx_data_path,cdate,title_fig,PDY,fld_min,fld_max):
    logging.info(f''' ========== PLOT: SCATTER ==========''')
    
    # Set the path to Natural Earth dataset
    cartopy.config['data_dir']=yaml_data['cartopy_ne_path']

    field_mean=float("{:.2f}".format(np.mean(np.absolute(omb))))
    field_std=float("{:.2f}".format(np.std(np.absolute(omb))))
    field_max=float("{:.2f}".format(np.max(np.absolute(omb))))
    field_min=float("{:.2f}".format(np.min(np.absolute(omb))))
    logging.info(f''' Mean |OMB|= {field_mean}''')
    logging.info(f''' STDV |OMB|= {field_std}''')
    logging.info(f''' Max |OMB|= {field_max}''')
    logging.info(f''' Min |OMB|= {field_min}''')

    # Print out OMB values to file
    hofx_data_fn=f'''hofx_omb_timehis_abs_{svar}.txt'''
    hofx_data_fp=os.path.join(hofx_data_path,hofx_data_fn)
    if os.path.exists(hofx_data_fp):
        # Remove line for same date
        with open(hofx_data_fp, 'r') as f:
            lines = f.readlines()
        with open(hofx_data_fp, 'w') as f:
            for line in lines:
                columns = line.strip().split(' ')
                if columns and columns[0].strip() != cdate:
                    f.write(line)
                    
    with open(hofx_data_fp, 'a') as f:
        print(cdate,field_mean,field_std,field_max,field_min, file=f)

    crs=ccrs.PlateCarree()
    fig=plt.figure(figsize=(8,5))
    ax=plt.subplot(111, projection=crs)
    coastline=cfeature.NaturalEarthFeature('physical','coastline','50m',edgecolor='black',facecolor='none',
                      linewidth=0.5,alpha=0.7)
    ax.add_feature(coastline)
    norm=plt.Normalize(fld_min,fld_max)
    num_cmap=25
    cmap_neg=mpl.colormaps['Blues_r'].resampled(num_cmap)
    cmap_pos=mpl.colormaps['Reds'].resampled(num_cmap)
    cmap_color=np.vstack((cmap_neg(np.linspace(0.1,0.7,num_cmap)),cmap_pos(np.linspace(0.2,0.8,num_cmap))))
    cmap_new=ListedColormap(cmap_color, name='BlueRed_rw')
    sc=ax.scatter(lon, lat, c=omb, s=1.5, cmap=cmap_new, transform=crs, norm=norm)
    cbar=plt.colorbar(sc, orientation="horizontal", shrink=0.5, pad=0.05)
    stitle=title_fig+' \n '+'Mean |OMB| ='+str(field_mean)+', STDV |OMB| ='+str(field_std)
    plt.title(stitle)
    output_fn=f'''hofx_omb_{svar}_{PDY}_scatter.png'''
    plt.savefig(output_fn,dpi=200,bbox_inches='tight')
    plt.close('all')


def plot_histogram(omb,svar,hofx_data_path,cdate,title_fig,PDY):
    logging.info(f''' ========== PLOT: HISTOGRAM ==========''')    
    field_mean=float("{:.2f}".format(np.mean(omb)))
    field_std=float("{:.2f}".format(np.std(omb)))
    field_max=float("{:.2f}".format(np.max(omb)))
    field_min=float("{:.2f}".format(np.min(omb)))
    logging.info(f''' Mean OMB= {field_mean}''')
    logging.info(f''' STDV OMB= {field_std}''')
    logging.info(f''' Max OMB= {field_max}''')
    logging.info(f''' Min OMB= {field_min}''')

    # Print out OMB values to file
    hofx_data_fn=f'''hofx_omb_timehis_{svar}.txt'''
    hofx_data_fp=os.path.join(hofx_data_path,hofx_data_fn)
    if os.path.exists(hofx_data_fp):
        # Remove line for same date
        with open(hofx_data_fp, 'r') as f:
            lines = f.readlines()
        with open(hofx_data_fp, 'w') as f:
            for line in lines:
                columns = line.strip().split(' ')
                if columns and columns[0].strip() != cdate:
                    f.write(line)

    with open(hofx_data_fp, 'a') as f:
        print(cdate,field_mean,field_std,field_max,field_min, file=f)

    nbins=yaml_data['nbins']

    fld_abs = max(abs(field_min),abs(field_max))
    fld_max = int(fld_abs)
    fld_min = -fld_max

    xlimit=[fld_min,fld_max]
    logging.info(f''' xlimit min= {fld_min}''')
    logging.info(f''' xlimit max= {fld_max}''')
    logging.info(f''' xlimit= {xlimit}''')
        
    plt.hist(omb[:], bins=nbins, range=xlimit, density=True, color ="blue")
    stitle=title_fig+' \n '+'Mean(OMB) ='+str(field_mean)+', STDV(OMB) ='+str(field_std)
    plt.title(stitle)
    output_fn=f'''hofx_omb_{svar}_{PDY}_histogram.png'''
    plt.savefig(output_fn,dpi=150,bbox_inches='tight')
    plt.close('all')

    return fld_min,fld_max


if __name__ == '__main__':
    global yaml_data

    yaml_file="plot_hofx_stats.yaml"
    with open(yaml_file, 'r') as f:
        yaml_data=yaml.load(f, Loader=yaml.FullLoader)
    f.close()

    cdate = yaml_data['cdate']
    TYPE_ANAL_FCST = yaml_data['TYPE_ANAL_FCST']
    hofx_data_path = yaml_data['hofx_data_path']
    JEDI_ALGORITHM = yaml_data['JEDI_ALGORITHM']
    JEDI_TYPE_FV3 = yaml_data['JEDI_TYPE_FV3']
    JEDI_TYPE_SOCA = yaml_data['JEDI_TYPE_SOCA']
    work_dir = yaml_data['work_dir']
    OBS_ATM_AMV_ABI_GOES_16 = yaml_data['OBS_ATM_AMV_ABI_GOES_16']
    OBS_ATM_ASCAT_W = yaml_data['OBS_ATM_ASCAT_W']
    OBS_ATM_ATMS_N20= yaml_data['OBS_ATM_ATMS_N20']
    OBS_ATM_CONVENTIONAL_PS = yaml_data['OBS_ATM_CONVENTIONAL_PS']
    OBS_ATM_GNSSRO_COSMIC2 = yaml_data['OBS_ATM_GNSSRO_COSMIC2']
    OBS_ATM_OZONE_OMPSNP_NPP = yaml_data['OBS_ATM_OZONE_OMPSNP_NPP']
    OBS_ATM_OZONE_OMPSTC_NPP = yaml_data['OBS_ATM_OZONE_OMPSTC_NPP']
    OBS_SNOW_GHCN = yaml_data['OBS_SNOW_GHCN']
    OBS_SNOW_IMS = yaml_data['OBS_SNOW_IMS']
    OBS_SNOW_SFCSNO = yaml_data['OBS_SNOW_SFCSNO']
    OBS_SWC_SMAP = yaml_data['OBS_SWC_SMAP']
    OBS_SWC_SMOPS = yaml_data['OBS_SWC_SMOPS']
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

    svar_list = []
    if JEDI_TYPE_SOCA == "YES":
        if TYPE_ANAL_FCST == "ctest":
            svar_list += ["ADT","InsituSalinity","InsituTemperature","SeaSurfaceSalinity","SeaSurfaceTemp"]
            if JEDI_ALGORITHM == "3dvar":
                svar_list += ["CoolSkin","SeaIceFraction"]
        else:
            svar_list += ["ADT","InsituSalinity","InsituTemperature","SeaSurfaceSalinity","SeaSurfaceTemp"]
    if JEDI_TYPE_FV3 == "YES":
        if TYPE_ANAL_FCST == "ctest":
            svar_list = ["NO2"]
    if OBS_ATM_AMV_ABI_GOES_16 == "YES":
        svar_list.append("satwnd.abi_goes-16")
    if OBS_ATM_ASCAT_W == "YES":
        svar_list.append("scatwnd.ascat_metop-b")
    if OBS_ATM_ATMS_N20 == "YES":
        svar_list.append("atms_n20")
    if OBS_ATM_CONVENTIONAL_PS == "YES":
        svar_list.append("conventional_ps")
    if OBS_ATM_GNSSRO_COSMIC2 == "YES":
        svar_list.append("gnssro_cosmic2")
    if OBS_ATM_OZONE_OMPSNP_NPP == "YES":
        svar_list.append("ozone.ompsnp_npp")
    if OBS_ATM_OZONE_OMPSTC_NPP == "YES":
        svar_list.append("ozone.ompstc_npp")
    if OBS_SNOW_GHCN == "YES":
        svar_list.append("ghcn_snow")
    if OBS_SNOW_IMS == "YES":
        svar_list.append("ims_snow")
    if OBS_SNOW_SFCSNO == "YES":
        svar_list.append("sfcsno")
    if OBS_SWC_SMAP == "YES":
        svar_list.append("smap_soil_moisture")
    if OBS_SWC_SMOPS == "YES":
        svar_list.append("smops_soil_moisture")

    logging.info(f''' svar_list: {svar_list}''')

    # svar: netcdf file name, svar_long: variable name in nc file
    for svar in svar_list:
        fn_input = f'''diag.{svar}_{PDY}{cyc}.nc'''
        logging.info(f''' Input file: {fn_input}''')
        fp_input = os.path.join(work_dir,fn_input)

        if svar == "ghcn_snow" or svar == "ims_snow" or svar == "sfcsno":
            svar_long = "totalSnowDepth"
        elif svar == "smap_soil_moisture" or svar == "smops_soil_moisture":
            svar_long = "soilMoistureVolumetric"
        elif svar == "ADT":
            svar_long = "absoluteDynamicTopography"
        elif svar == "CoolSkin":
            svar_long = "seaSurfaceTemperature"
        elif svar == "InsituSalinity":
            svar_long = "salinity"
        elif svar == "InsituTemperature":
            svar_long = "waterTemperature"
        elif svar == "SeaIceFraction":
            svar_long = "seaIceFraction"
        elif svar == "SeaSurfaceSalinity":
            svar_long = "seaSurfaceSalinity"
        elif svar == "SeaSurfaceTemp":
            svar_long = "seaSurfaceTemperature"
        elif svar == "NO2":
            svar_long = "nitrogendioxideColumn"
        elif svar == "atms_n20":
            svar_long = "brightnessTemperature"
        elif svar == "conventional_ps":
            svar_long = "stationPressure"
        elif svar == "gnssro_cosmic2":
            svar_long = "bendingAngle"
        elif svar == "ozone.ompsnp_npp":
            svar_long = "ozoneLayer"
        elif svar == "ozone.ompstc_npp":
            svar_long = "ozoneTotal"
        elif svar == "satwnd.abi_goes-16":
            svar_long = "windEastward"
        elif svar == "scatwnd.ascat_metop-b":
            svar_long = "windEastward"
        else:
            svar_long = svar

        omb,lat,lon=get_obs_stats(fp_input,svar_long)

        title_fig=f'''{svar}::Obs-Bkg::{PDY}'''
        fld_min,fld_max = plot_histogram(omb,svar,hofx_data_path,cdate,title_fig,PDY)       
        plot_scatter(omb,svar,hofx_data_path,cdate,title_fig,PDY,fld_min,fld_max)

