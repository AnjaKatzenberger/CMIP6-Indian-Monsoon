#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 17:35:27 2020

@author: anjakatzenberger
"""

import netCDF4 as nc
import os

###############################################################
#           EXTRACTING MEAN FROM NETCDF-FILES                 #
#                   Anja Katzenberger                         #
#           anja.katzenberger@pik-potsdam.de                  #
#                       18.06.2020                            #
###############################################################
# Extracts calculated mean from NetCDF files to python

# Directories with files of interest
indir = "/home/anjaka/mean_pr/mean_pr_ssp585"

# Specify period of interest
h_start = "1850"
h_end = "1879"
r_start = "2070"
r_end = "2099"
c_end = "2100"

#### Extracting pr data
for folder in [f.name for f in os.scandir(indir)]: 
    ssp = folder[8:]
    dir = os.sep.join((indir,folder))
    files = next(os.walk(dir))[2]

    name_h = "pr_"+ ssp + "_" + h_start + "_" + h_end
    name_r = "pr_"+ ssp + "_" + r_start + "_" + r_end
    name_c = "pr_"+ ssp + "_" + h_start + "_" + c_end
    
    pr_h = []
    pr_r = []
    pr_c = []
    pr_h_model = []
    pr_r_model = []
    pr_c_model = []

    # historical
    for file in files:
        dir_file = os.sep.join((dir, file))
        data = nc.Dataset(dir_file)
        
        if file.endswith("_" + h_start + "-" + h_end + "_India_JJASmean_ymonmean_fldmean.nc"):
            center_model = file.split('_' + h_start)[0][3:]
            model = center_model.split('_')[1]
            pr = data['pr'][0,0,0]
            pr = pr.data * 86400
            pr_h.append(pr)
            pr_h_model.append(model)
    
    # future: ssp585
        if file.endswith("_" + ssp + "_" + r_start+ "-" + r_end + "_India_JJASmean_ymonmean_fldmean.nc"):
            center_model = file.split('_' + ssp)[0][3:]
            model = center_model.split('_')[1]
            pr = data['pr'][0,0,0]
            pr = pr.data * 86400
            pr_r.append(pr)
            pr_r_model.append(model)
                  
    # combined: 1850-2100
        if file.endswith("_" + ssp + "_" + h_start + "-" + c_end + "_India_JJASmean_fldmean.nc"):
            center_model = file.split('_' + ssp)[0][3:]
            model = center_model.split('_')[1]
            pr = data['pr'][:]
            pr = pr.data * 86400
            pr_c_i = []
            for i in range(len(pr)):
                pr_i = pr[i][0][0]
                pr_c_i.append(pr_i)
            pr_c.append(pr_c_i)
            pr_c_model.append(model)
            print(pr_c)
            print(pr_c_model)
     
    
   

        
