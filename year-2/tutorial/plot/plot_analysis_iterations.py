#!/usr/bin/env python3

###################################################################### CHJ #####
## Name		: plot_analysis_iterations.py
## Usage	: Plot analysis info over iterations
###################################################################### CHJ #####

import os, sys
import logging
import pathlib
import yaml
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.ticker
import matplotlib as mpl


# Main part (will be called at the end) ============================= CHJ =====
def main():

    yaml_file="plot_analysis_iterations.yaml"
    with open(yaml_file, 'r') as f:
        yaml_data=yaml.load(f, Loader=yaml.FullLoader)
    f.close()

    TYPE_ANAL_FCST = yaml_data['TYPE_ANAL_FCST']
    fn_data_log = yaml_data['fn_data_log']
    JEDI_ALGORITHM = yaml_data['JEDI_ALGORITHM']
    JEDI_TYPE_SOCA = yaml_data['JEDI_TYPE_SOCA']
    out_fn_base = yaml_data['out_fn_base']
    OBS_ATM_AMV_ABI_GOES_16 = yaml_data['OBS_ATM_AMV_ABI_GOES_16']
    OBS_ATM_ASCAT_W = yaml_data['OBS_ATM_ASCAT_W']
    OBS_ATM_ATMS_N20= yaml_data['OBS_ATM_ATMS_N20']
    OBS_ATM_CONVENTIONAL_PS = yaml_data['OBS_ATM_CONVENTIONAL_PS']
    OBS_ATM_GNSSRO_COSMIC2 = yaml_data['OBS_ATM_GNSSRO_COSMIC2']
    OBS_SNOW_GHCN = yaml_data['OBS_SNOW_GHCN']
    OBS_SNOW_IMS = yaml_data['OBS_SNOW_IMS']
    OBS_SNOW_SFCSNO = yaml_data['OBS_SNOW_SFCSNO']
    OBS_SWC_SMAP = yaml_data['OBS_SWC_SMAP']
    OBS_SWC_SMOPS = yaml_data['OBS_SWC_SMOPS']
    path_data = yaml_data['path_data']
    PY_LOG_LEVEL=yaml_data['PY_LOG_LEVEL']
    work_dir = yaml_data['work_dir']

    # Set logging config
    log_level_str = PY_LOG_LEVEL.upper()
    try:
        log_level = getattr(logging, log_level_str)
    except AttributeError:
        log_level_str = "INFO"
        log_level = logging.INFO
        print(f''' WARNING: Invalid log level "{PY_LOG_LEVEL.upper()}", set to INFO.''')
    print(f''' Python Log Level= str: {log_level_str}, attr: {log_level}''')
    logging.basicConfig(format='%(levelname)s::%(filename)s::L%(lineno)d::%(message)s', level=log_level)

    logging.info(f''' YAML Data: {yaml_data}''')

    svar_list = []
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
    if JEDI_TYPE_SOCA == "YES":
        if TYPE_ANAL_FCST == "ctest":
            svar_list += ["ADT","InsituSalinity","InsituTemperature","SeaSurfaceSalinity","SeaSurfaceTemp"]
            if JEDI_ALGORITHM == "3dvar":
                svar_list += ["CoolSkin","SeaIceFraction"]
        else:
            svar_list += ["ADT","InsituSalinity","InsituTemperature","SeaSurfaceSalinity","SeaSurfaceTemp"]
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

    # Path to input file
    fp_data_log = os.path.join(path_data,fn_data_log)

    # Variable name of observations
    for svar in svar_list:
        num_ch = 1
        if svar == "ghcn_snow" or svar == "ims_snow" or svar == "sfcsno":
            var_nm = "totalSnowDepth"
            qc_str_obs = svar
        elif svar == "smap_soil_moisture":
            var_nm = "soilMoistureVolumetric"
            qc_str_obs = "SoilMoistureSMAP"
        elif svar == "smops_soil_moisture":
            var_nm = "soilMoistureVolumetric"
            qc_str_obs = "SoilMoiistureSMOPS"
        elif svar == "ADT":
            var_nm = "absoluteDynamicTopography"
            qc_str_obs = svar
        elif svar == "CoolSkin":
            var_nm = "seaSurfaceTemperature"
            qc_str_obs = svar
        elif svar == "InsituSalinity":
            var_nm = "salinity"
            qc_str_obs = svar
        elif svar == "InsituTemperature":
            var_nm = "waterTemperature"
            qc_str_obs = svar
        elif svar == "SeaIceFraction":
            var_nm = "seaIceFraction"
            qc_str_obs = svar
        elif svar == "SeaSurfaceSalinity":
            var_nm = "seaSurfaceSalinity"
            qc_str_obs = svar
        elif svar == "SeaSurfaceTemp":
            var_nm = "seaSurfaceTemperature"
            qc_str_obs = svar
        elif svar == "atms_n20":
            var_nm = "brightnessTemperature"
            qc_str_obs = "ATMS N20"
            num_ch = 22
        elif svar == "conventional_ps":
            var_nm = "stationPressure"
            qc_str_obs = svar
        elif svar == "gnssro_cosmic2":
            var_nm = "bendingAngle"
            qc_str_obs = svar
        elif svar == "satwnd.abi_goes-16":
            var_nm = "windEastward"
            qc_str_obs = "satwind_goes-16"
        elif svar == "scatwnd.ascat_metop-b":
            var_nm = "windEastward"
            qc_str_obs = "ascatw_ascat_metop-b"
        else:
            var_nm = svar
            qc_str_obs = svar

        plot_data_log(fp_data_log,svar,var_nm,qc_str_obs,num_ch,out_fn_base,work_dir)


# Plot data from files =============================================== CHJ =====
def plot_data_log(fp_data_log,svar,var_nm,qc_str_obs,num_ch,out_fn_base,work_dir):

    logging.info(f''' === svar: '{svar}' === obs string: '{qc_str_obs}' === var name: '{var_nm}' === ''')

    for ichm1 in range(num_ch):
        if num_ch > 1:
            ich = ichm1 + 1
            nobs_qc_prefix = f'''QC {qc_str_obs} {var_nm}_{ich}'''
        else:
            nobs_qc_prefix = f'''QC {qc_str_obs} {var_nm}'''
        nobs_qc_suffix = "observations.\n"
        logging.info(f''' QC prefix for Nobs: {nobs_qc_prefix}''')
        logging.debug(f''' QC suffix for Nobs: {nobs_qc_suffix}''')

        nobs_qc_iter = []
        nobs_in_iter = []
        i_cnt = 0
        n_iter = []
        with open(fp_data_log, 'r') as file:
            for line in file:
                if line.startswith(nobs_qc_prefix) and line.endswith(nobs_qc_suffix):
                    line_data_raw = line
                    line_split = line.split(': ')[1].split(' ')
                    if line_split[1] == "passed" and line_split[2] == "out" and line_split[3] == "of":
                        i_cnt = i_cnt + 1
                        n_iter.append(i_cnt)
                        nobs_qc_val = int(line_split[0])
                        nobs_qc_iter.append(nobs_qc_val)
                        nobs_in_val = int(line_split[4])
                        nobs_in_iter.append(nobs_in_val)
                        #print(f'''Iter.={i_cnt}, Nobs_QC={nobs_qc_val}, Nobs_in={nobs_in_val}''')

        logging.info(f'''Iteration: {n_iter}''')
        logging.info(f'''Nobs_QC: {nobs_qc_iter}''')
        logging.info(f'''Nobs_in: {nobs_in_iter}''')

        qc_str_obs_upper = qc_str_obs.upper()
        if num_ch == 1:
            out_title_obs = f'''OBS QC::{qc_str_obs_upper}'''
            out_fn_obs = f'''{out_fn_base}_obs_qc_{svar}'''
        else:
            out_title_obs = f'''OBS QC::{qc_str_obs_upper}::CH{ich}'''
            out_fn_obs = f'''{out_fn_base}_obs_qc_{svar}_ch{ich}'''

        x = np.arange(len(n_iter))

        txt_fnt=7
        bar_wdth=0.1
        bar_half=bar_wdth*0.5
        # figsize=(width,height) in inches
        fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True, figsize=(5,2))
        ax.bar(x-bar_half, nobs_in_iter, bar_wdth, color='blue', label='Nobs:raw')
        ax.bar(x+bar_half, nobs_qc_iter, bar_wdth, color='red', label='Nobs:QC')

        ax.set_xticks(x)
        ax.set_xticklabels(n_iter)
        ax.set_xlabel('Iteration', fontsize=txt_fnt-1)
        ax.set_ylabel('Number of observations', fontsize=txt_fnt-1)
        ax.set_title(out_title_obs, fontsize=txt_fnt)
        ax.tick_params(axis="x",labelsize=txt_fnt-2)
        ax.tick_params(axis="y",labelsize=txt_fnt-2)
        ax.legend(fontsize=txt_fnt-3, loc='upper right',bbox_to_anchor=(1,-0.15),ncol=2)
        ax.grid(linewidth=0.1)

#        plt.xticks(rotation=30, ha='right')
        plt.tight_layout()
        # Output figure
        ndpi = 300
        out_file(work_dir,out_fn_obs,ndpi)


# Output file ======================================================= CHJ =====
def out_file(work_dir,out_file,ndpi):
    # Output figure
    fp_out = os.path.join(work_dir,out_file)
    plt.savefig(fp_out+'.png',dpi=ndpi,bbox_inches='tight')
    plt.close('all')


# Main call ========================================================= CHJ =====
if __name__=='__main__':
    main()

