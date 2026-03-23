#!/usr/bin/env python3

###################################################################### CHJ #####
## Name		: plot_cubed_sphere_grid.py
## Usage	: Plot cubed sphere grid file in UFS DA workflow
## NOAA/EPIC
## History ===============================
## V000: 2026/02/23: Chan-Hoo Jeon : Preliminary version
## V001: 2026/02/24: Chan-Hoo Jeon : Add increment plot
###################################################################### CHJ #####

import os, sys
import logging
import yaml
import numpy as np
import netCDF4 as nc
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr
from scipy.stats import norm
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.ticker
import matplotlib as mpl
from matplotlib.colors import ListedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable


# Main part (will be called at the end) ============================= CHJ =====
def main():
    global num_tiles

    yaml_file = "plot_cubed_sphere_grid.yaml"
    with open(yaml_file, 'r') as f:
        yaml_data = yaml.load(f, Loader=yaml.FullLoader)
    f.close()

    cartopy_ne_path = yaml_data['cartopy_ne_path']
    colorbar_option = yaml_data['colorbar_option']
    fn_data_atm = yaml_data['fn_data_atm']
    fn_data_sfc = yaml_data['fn_data_sfc']
    fn_data_inc_atm = yaml_data['fn_data_inc_atm']
    fn_data_inc_sfc = yaml_data['fn_data_inc_sfc']
    out_title_base = yaml_data['out_title_base']
    out_fn_base = yaml_data['out_fn_base']
    path_data = yaml_data['path_data']
    path_data_inc = yaml_data['path_data_inc']
    plot_increment_atm = yaml_data['plot_increment_atm']
    plot_increment_sfc = yaml_data['plot_increment_sfc']
    PY_LOG_LEVEL = yaml_data['PY_LOG_LEVEL']
    var_list_atm = yaml_data['var_list_atm']
    var_list_sfc = yaml_data['var_list_sfc']
    work_dir = yaml_data['work_dir']
    zlvl_atm = yaml_data['zlevel_number_atm']
    zlvl_sfc = yaml_data['zlevel_number_sfc']

    num_tiles = 6
    zlvlm1_atm = int(zlvl_atm)-1
    zlvlm1_sfc = int(zlvl_sfc)-1

    # Set logging config
    log_level_str = PY_LOG_LEVEL.upper()
    try:
        log_level = getattr(logging, log_level_str)
    except AttributeError:
        log_level_str = "INFO"
        log_level = logging.INFO
        print(f''' WARNING: Invalid log level "{PY_LOG_LEVEL.upper()}", set to INFO.''')
    print(f''' Python Log Level = str: {log_level_str}, attr: {log_level}''')
    logging.basicConfig(format='%(levelname)s::%(pathname)s::L%(lineno)d::%(message)s', level=log_level)

    logging.info(f''' YAML Data: {yaml_data}''')

    # Set the path to Natural Earth dataset
    cartopy.config['data_dir'] = cartopy_ne_path

    # get lon, lat
    glon_atm,glat_atm = get_geo(path_data,fn_data_atm)
    glon_sfc,glat_sfc = get_geo(path_data,fn_data_sfc)

    # plot atm file
    if var_list_atm:
        for var_nm in var_list_atm:
            plot_data(path_data,fn_data_atm,var_nm,zlvlm1_atm,out_title_base,
                      out_fn_base,glon_atm,glat_atm,work_dir,colorbar_option,"bkg")
    # plot sfc file
    if var_list_sfc:
        for var_nm in var_list_sfc:
            plot_data(path_data,fn_data_sfc,var_nm,zlvlm1_sfc,out_title_base,
                      out_fn_base,glon_sfc,glat_sfc,work_dir,colorbar_option,"bkg")
    # Plot atm increment
    if plot_increment_atm == "YES":
        if var_list_atm:
            for var_nm in var_list_atm:
                plot_data(path_data_inc,fn_data_inc_atm,var_nm,zlvlm1_atm,out_title_base,
                          out_fn_base,glon_atm,glat_atm,work_dir,"real","inc")
    # Plot sfc increment
    if plot_increment_sfc == "YES":
        if var_list_sfc:
            for var_nm in var_list_sfc:
                plot_data(path_data_inc,fn_data_inc_sfc,var_nm,zlvlm1_atm,out_title_base,
                          out_fn_base,glon_sfc,glat_sfc,work_dir,"real","inc")


# geo lon/lat from =================================================== CHJ =====
def get_geo(path_data,fn_data):

    logging.info(f''' ===== geo data: {fn_data} ===========================''')
    fp_data = os.path.join(path_data,fn_data)
    try: mdata = xr.open_dataset(fp_data)
    except: raise Exception('Could NOT find the file',fp_data)

    # Extract longitudes, and latitudes
    glon = np.ma.masked_invalid(mdata['lon'].data)
    glat = np.ma.masked_invalid(mdata['lat'].data)

    logging.info(f''' Dimension of glon = {glon.shape}''')
    logging.info(f''' glon, max = {np.max(glon)}''')
    logging.info(f''' glat, min = {np.min(glon)}''')
    logging.info(f''' Dimension of glat = {glat.shape}''')
    logging.info(f''' glat, max = {np.max(glat)}''')
    logging.info(f''' glat, min = {np.min(glat)}''')

    return glon,glat


# Get sfc_data from files and plot ================================== CHJ =====
def plot_data(path_data,fn_data,var_nm,zlvlm1,out_title_base,out_fn_base,
              glon,glat,work_dir,colorbar_option,inc_opt):

    # center of map
    c_lon = -77.0369
    zlvl = zlvlm1+1

    logging.info(f''' ===== {fn_data}:: '{var_nm}' ========================''')
    # open the data file
    fp_data = os.path.join(path_data,fn_data)
    try: data_raw = xr.open_dataset(fp_data)
    except: raise Exception('Could NOT find the file',fp_data)
    logging.info(f''' Variables: {list(data_raw.variables)}''')

    # Extract valid variable
    var_orig = data_raw[var_nm]
    var_data = np.ma.masked_invalid(var_orig.values)
    var_nm_long = var_orig.attrs.get("long_name", "No long-name attribute found")
    var_nm_unit = var_orig.attrs.get("units", "No units attribute found")
    logging.info(f''' Variable: long name = {var_nm_long}''')
    logging.info(f''' Variable: unit = {var_nm_unit}''')
    logging.info(f''' Dimension of original data = {var_data.shape}''')
    # Squeeze time dimension
    var_data_m1 = np.squeeze(var_data)
    logging.info(f''' Dimension of squeezed data = {var_data_m1.shape}''')
    ndim_var = var_data_m1.ndim
    logging.info(f''' Variable: number of dimensions = {ndim_var}''')
    if ndim_var == 4:
        var_data_xy = var_data_m1[:,zlvlm1,:,:]
        var_data_2d6 = np.squeeze(var_data_xy)
    else:
        var_data_2d6 = np.squeeze(var_data)

    logging.info(f''' Dimension of data = {var_data_2d6.shape}''')
    logging.info(f''' Max = {np.max(var_data_2d6)}''')
    logging.info(f''' Min = {np.min(var_data_2d6)}''')

    data_raw.close()

    cbar_extend = 'neither'
    cbar_label = f'''{var_nm_long} ({var_nm_unit})'''

    if inc_opt == "inc":
        cs_cmap = 'seismic'
        cbar_label = '\u0394'+cbar_label
        var_max = np.nanmax(var_data_2d6)
        var_min = np.nanmin(var_data_2d6)
        if var_max == var_min:
            cs_max = max(abs(var_max),abs(var_min))+0.1
            cs_min = cs_max*-1.0
        else:
            cs_max = max(abs(var_max),abs(var_min))
            cs_min = cs_max*-1.0
    else:
        # cs_cmap options
        if var_nm == "o3mr":
            cs_cmap = 'turbo'
        elif var_nm == "spfh" or var_nm == "spfh2m" or var_nm == "snod":
            cs_cmap = 'gist_ncar_r'
        elif var_nm == "tmp" or var_nm == "tmp2m":
            cs_cmap = 'jet'
        elif var_nm == "ugrd" or var_nm == "vgrd":
            cs_cmap = 'seismic'
        elif var_nm == "soilm":
            cs_cmap = 'gist_ncar'
        else:
            cs_cmap = 'gist_ncar_r'
        # cs_max,min / cbar_extend
        if colorbar_option == "fixed":
            if var_nm == "o3mr":
                cs_max = 3.0e-7
                cs_min = 2.0e-7
                cbar_extend = 'both'
            elif var_nm == "spfh":
                cs_max = 4.0e-6
                cs_min = 2.0e-6
                cbar_extend = 'both'
            elif var_nm == "tmp":
                cs_max = 188.0
                cs_min = 170.0
                cbar_extend = 'both'
            elif var_nm == "ugrd":
                cs_max = 80.0
                cs_min = -80.0
                cbar_extend = 'both'
            elif var_nm == "vgrd":
                cs_max = 80.0
                cs_min = -80.0
                cbar_extend = 'both'
            elif var_nm == "snod":
                cs_max = 2.0
                cs_min = 0.0
                cbar_extend = 'max'
            elif var_nm == "soilm":
                cs_max = 1000.0
                cs_min = 0.0
                cbar_extend = 'max'
            elif var_nm == "spfh2m":
                cs_max = 0.02
                cs_min = 0.0
                cbar_extend = 'max'
            elif var_nm == "tmp2m":
                cs_max = 310.0
                cs_min = 230.0
                cbar_extend = 'both'
            else:
                cs_max = np.nanmax(var_data_2d6)
                cs_min = np.nanmin(var_data_2d6)
        else:
            cs_max = np.nanmax(var_data_2d6)
            cs_min = np.nanmin(var_data_2d6)

    logging.info(f''' colorbar_option = {colorbar_option}''')
    logging.info(f''' cs_max = {cs_max}''')
    logging.info(f''' cs_min = {cs_min}''')
    logging.info(f''' colorbar_extend = {cbar_extend}''')

    # Plot all tiles together
    if inc_opt == "inc":
        out_title_base = f'''{out_title_base}INC::'''
        out_fn_base = f'''{out_fn_base}inc_'''

    if ndim_var == 4:
        out_title = f'''{out_title_base}{var_nm}::L{zlvl}'''
        out_fn = f'''{out_fn_base}{var_nm}_z{zlvl}'''
    else:
        out_title = f'''{out_title_base}{var_nm}'''
        out_fn = f'''{out_fn_base}{var_nm}'''

    fig,ax=plt.subplots(1,1,subplot_kw=dict(projection=ccrs.Robinson(c_lon)))
    ax.set_title(out_title, fontsize=6)
    # Call background plot
    back_plot(ax)
    for it in range(num_tiles):
        itp=it+1
        glon_tile=np.squeeze(glon[it,:,:])
        if itp == 1:
            glon_tile=(glon_tile+180)%360-180
        glat_tile=np.squeeze(glat[it,:,:])
        var_tile=np.squeeze(var_data_2d6[it,:,:])
        cs=ax.pcolormesh(glon_tile,glat_tile,var_tile,cmap=cs_cmap,rasterized=True,
           vmin=cs_min,vmax=cs_max,transform=ccrs.PlateCarree())
    divider=make_axes_locatable(ax)
    ax_cb=divider.new_horizontal(size="3%",pad=0.1,axes_class=plt.Axes)
    fig.add_axes(ax_cb)
    cbar=plt.colorbar(cs,cax=ax_cb,extend=cbar_extend)
    cbar.ax.tick_params(labelsize=6)
    cbar.set_label(cbar_label,fontsize=6)
    # Output figure
    ndpi = 300
    out_file(work_dir,out_fn,ndpi)


# Background plot ==================================================== CHJ =====
def back_plot(ax):
    # Resolution of background natural earth data ('50m' or '110m')
    back_res = '50m'

    fline_wd = 0.5  # line width
    falpha = 0.7 # transparency

    # natural_earth
    land = cfeature.NaturalEarthFeature('physical','land',back_res,
                      edgecolor='face',facecolor=cfeature.COLORS['land'],
                      alpha=falpha)
    lakes = cfeature.NaturalEarthFeature('physical','lakes',back_res,
                      edgecolor='blue',facecolor='none',
                      linewidth=fline_wd,alpha=falpha)
    coastline = cfeature.NaturalEarthFeature('physical','coastline',
                      back_res,edgecolor='black',facecolor='none',
                      linewidth=fline_wd,alpha=falpha)
    states = cfeature.NaturalEarthFeature('cultural','admin_1_states_provinces',
                      back_res,edgecolor='green',facecolor='none',
                      linewidth=fline_wd,linestyle=':',alpha=falpha)
    borders = cfeature.NaturalEarthFeature('cultural','admin_0_countries',
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
    fp_out = os.path.join(work_dir,out_file)
    plt.savefig(fp_out+'.png',dpi=ndpi,bbox_inches='tight')
    plt.close('all')


# Main call ========================================================= CHJ =====
if __name__=='__main__':
    main()

