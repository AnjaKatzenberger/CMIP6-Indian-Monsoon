#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 10:05:05 2020

@author: anjakatzenberger
"""
#!/usr/bin/python
import os
import subprocess

###############################################################
#               APPLYING CDOs ON CMIP6 MODELS                 #
#            EXAMPLE: GISS-E2-1-G (CENTER: NASA-GISS)         #
#                   Anja Katzenberger                         #
#           anja.katzenberger@pik-potsdam.de                  #
#                       10.06.2020                            #
###############################################################
# Applying CDOs on GISS-E2-1-G as example
# This data processing was done automatized for all 32 models in the study

# Data directories for historical and future (here: ssp126) CMIP6 precipitation data and output directory
hdir = os.path.abspath("")
rdir = os.path.abspath("")
outdir = os.path.abspath("")
loc_landmask = ""

# Specify Variable, Table, Model, Member, grid type and Scenario
vbl = 'pr'
table = 'Amon'
center = 'NASA-GISS'
model = 'GISS-E2-1-G'
member = 'r1i1p1f2'
grid = 'gn'
ssp = 'ssp126'

# Creating list of historical and future files
hfiles = os.listdir(hdir)
rfiles = os.listdir(rdir)

# Choosing years of interest for historic and future period
hstartyear = 1850
hendyear = 1879
rstartyear = 2070
rendyear = 2099

### landmask
files = os.listdir(loc_landmask)

models_m = []
for file in files:
    model_m = file.split('_')[2]
    models_m.append(model_m)

#____________________
# Formulating CDO commands
#___________________

### Temporal Merging
# Merges all historical file to one file (1850-2015)
hist_output = os.sep.join((outdir, '_'.join((vbl, model, "1850-2015.nc"))))
cdo_cmd_hist_merge = ' '.join(("cdo -O mergetime ", os.sep.join((hdir, "*.nc")), hist_output))

# Merges all future files to one file (2015-2100)
r_output = os.sep.join((outdir, '_'.join((vbl, model, ssp, "2015-2100.nc"))))
cdo_cmd_r_merge = ' '.join(("cdo -O mergetime ", os.sep.join((rdir, "*.nc")), r_output))

# Creates one merged output with data (1850-2100)
comb_output = os.sep.join((outdir, '_'.join((vbl, model, ssp, "1850-2100.nc"))))
cdo_cmd_comb_merge = ' '.join(("cdo -O mergetime ", hist_output, r_output, comb_output))
    

### Focusing on land area: Applying individually created landmasks
print(model)
index_mask = 99        
mask_used = "GISS-E2-1-G"
mask_dir = os.sep.join((loc_landmask, "fx_sftlf_GISS-E2-1-G_masked_missval.nc")) 
   
    
mul_output = os.sep.join((outdir, '_'.join((vbl, center, model, ssp, "1850-2100_mask.nc"))))
cdo_cmd_mul = ' '.join(("cdo -O mul", mask_dir, comb_output, mul_output))
    
    

### Cutting box around India 
hist_output_India = os.sep.join((outdir, '_'.join((vbl, center, model, "1850-2015_India.nc"))))
nco_cmd_hist_India = "ncks -Od lon,67.5,98.0 -d lat,6.0,36.0 " + hist_output + " " + hist_output_India

r_output_India = os.sep.join((outdir, '_'.join((vbl, model, ssp, "2015-2100_India.nc"))))
nco_cmd_r_India = "ncks -Od lon,67.5,98.0 -d lat,6.0,36.0 " + r_output + " " + r_output_India

comb_output_India = os.sep.join((outdir, '_'.join((vbl, center, model, ssp, "mask_1850-2100_India.nc"))))
nco_cmd_comb_India = "ncks -Od lon,67.5,98.0 -d lat,6.0,36.0 " + mul_output + " " + comb_output_India


### Calculating Mean over JJAS
hist_output_JJASmean = os.sep.join((outdir, '_'.join((vbl, model, "1850-2015_India_JJASmean.nc"))))
cdo_cmd_hist_JJASmean = "cdo -O timselmean,4,5,8 " + hist_output_India + " " + hist_output_JJASmean

r_output_JJASmean = os.sep.join((outdir, '_'.join((vbl, model, ssp, "2015-2100_India_JJASmean.nc"))))
cdo_cmd_r_JJASmean = "cdo -O timselmean,4,5,8 " + r_output_India + " " + r_output_JJASmean

comb_output_JJASmean = os.sep.join((outdir, '_'.join((vbl, center, model, ssp, "1850-2100_mask_India_JJASmean.nc")))) 
cdo_cmd_comb_JJASmean = "cdo -O timselmean,4,5,8 " + comb_output_India + " " + comb_output_JJASmean #


### Calculatin Mean over 30 years
hist_output_ymonmean = os.sep.join((outdir, '_'.join((vbl, model, "1850-1880_India_JJASmean_ymonmean.nc"))))
cdo_cmd_hist_ymonmean = "cdo -O ymonmean -seldate," + str(hstartyear) + "-01-01," + str(hendyear) + "-12-31 " + hist_output_JJASmean + " " + hist_output_ymonmean #

r_output_ymonmean = os.sep.join((outdir, '_'.join((vbl, model, ssp, "2070-2100_India_JJASmean_ymonmean.nc"))))
cdo_cmd_r_ymonmean = "cdo -O ymonmean -seldate," + str(rstartyear) + "-01-01," + str(rendyear) + "-12-31 " + r_output_JJASmean + " " + r_output_ymonmean #


#fldmean
comb_output_fldmean = os.sep.join((outdir, '_'.join((vbl, center, model, ssp,  "1850-2100_mask_India_JJASmean_fldmean.nc"))))
cdo_cmd_comb_fldmean = "cdo -O fldmean " + comb_output_JJASmean + ' ' + comb_output_fldmean
        


#____________________
# Calling CDOs
#___________________
subprocess.check_call(cdo_cmd_hist_merge, shell=True)
subprocess.check_call(cdo_cmd_r_merge, shell=True)
subprocess.check_call(cdo_cmd_comb_merge, shell=True)
subprocess.check_call(cdo_cmd_mul, shell=True)
#subprocess.check_call(nco_cmd_hist_India, shell=True)
#subprocess.check_call(nco_cmd_r_India, shell=True)
subprocess.check_call(nco_cmd_comb_India, shell=True)
#subprocess.check_call(cdo_cmd_hist_JJASmean, shell=True)
#subprocess.check_call(cdo_cmd_r_JJASmean, shell=True)
subprocess.check_call(cdo_cmd_comb_JJASmean, shell=True)
#subprocess.check_call(cdo_cmd_hist_ymonmean, shell=True)
#subprocess.check_call(cdo_cmd_r_ymonmean, shell=True)
subprocess.check_call(cdo_cmd_comb_fldmean, shell=True)

#____________________
# Removing temporary files
#___________________
os.remove(hist_output)
os.remove(r_output)
os.remove(comb_output)
os.remove(mul_output)
#os.remove(hist_output_India)
#os.remove(r_output_India)
os.remove(comb_output_India)
#os.remove(r_output_JJASmean)
#os.remove(hist_output_JJASmean)
