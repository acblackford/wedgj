#Import necessary packages:
import numpy as np
import matplotlib.pyplot as plt
import cartopy as ccrs
import cartopy.feature as cfeature
from  datetime import datetime, timedelta
from wedgj import wedgj_utils
import os
import pygrib
import matplotlib.colors as mcolors

###########################################
#                                         #
#                 winter                  #
#                                         #
###########################################

class winter:

  def __init__(self):
    self.date = datetime.utcnow()
    
###--------- HRRR Ice Accretion Function ---------###

  def hrrr_ice(self, spath = None, domain = 'CONUS'):
  
    #Set up initial file and series of files:
    # Location of HRRR data:
    hrrr_url = "https://nomads.ncep.noaa.gov/pub/data/nccf/com/hrrr/prod/"

    # Build the HRRR urls
    urls = []
    date = datetime.utcnow()
    if (date.hour >= 21):
        date = date.replace(hour = 18)
    elif (date.hour >= 15):
        date = date.replace(hour = 12)
    elif (date.hour >= 9):
        date = date.replace(hour = 6)
    elif (date.hour >= 3):
        date = date.replace(hour = 0)
    else:
        date = date.replace(hour = 18)-timedelta(days=1)

    for i in range(49):
        urls.append(hrrr_url+"hrrr.{}/conus/hrrr.t{:02d}z.wrfprsf{:02d}.grib2".format(
            date.strftime("%Y%m%d"), date.hour, i))
            
    ### Loop over the run, downloading just the ice field:
    try:
        for i, url in enumerate(urls):
            # Download index file
            os.system("curl -o hrrr_index_ice {}".format(url+".idx"))

            # Open index file to find relevant bytes
            f = open("hrrr_index_ice", "r")
            lines = list(f)
            f.close()

            ### Do each variable in turn:
            data = {}
            for var in [("FRZR", "surface"),
                         ]: 

                # Check the index
                flag = False
                for line in lines:
                    # Check if var already found
                    if flag:
                        byte_end = line.split(":")[1]
                        break

                    # Locate variable
                    if ((var[0] in line) and (var[1] in line)):
                        byte_start = line.split(":")[1]
                        flag = True

                # Download the HRRR data
                os.system("curl -o hrrr_out_ice -r {}-{} {}".format(byte_start, byte_end, url))

                # Grab the data
                grib = pygrib.open("hrrr_out_ice")
                data[var[0]+var[1]] = grib[1].values
                lons = grib[1].longitudes.reshape(data[var[0]+var[1]].shape)
                lats = grib[1].latitudes.reshape(data[var[0]+var[1]].shape)
                vd = grib[1].validDate
                ad = grib[1].analDate
                grib.close()

            
            ice = data["FRZR"+"surface"] * 0.04
            ice[ice < 0.01] = np.nan

            #Plot Ice Accretion:
            figsize_table = wedgj_utils.figsize_table(self)

            #Make figure:
            fig, ax = plt.subplots(figsize = figsize_table[domain], subplot_kw = {'projection' : ccrs.crs.PlateCarree()})

            extent_table = wedgj_utils.extent_table(self)

            #Add cartopy boundaries::
            try:
              ax.set_extent(extent_table[domain])
            except:
              ax.set_extent(extent_table['CONUS'])
              print('Invalid Domain Input. Setting extent to CONUS.')
            
            ice_table = wedgj_utils.ice_cmap(self)
            
            barb_int = 16
            icecf = ax.contourf(lons, lats, ice, cmap=ice_table['ice_cmap'], levels = ice_table['ice_clevs'], norm= mcolors.BoundaryNorm(ice_table['ice_clevs'], ice_table['ice_cmap'].N), transform = ccrs.crs.PlateCarree(), extend = 'max')
            
            #Add counties if not CONUS:
            if domain != 'CONUS':
              wedgj_utils.plot_counties(self, ax)
            
            #Add cities to state plots:
            if domain == 'Ohio':
                wedgj_utils.plot_oh_cities(self, ax)
            elif domain == 'Indiana':
                wedgj_utils.plot_in_cities(self, ax)
            elif domain == 'Alabama':
                wedgj_utils.plot_al_cities(self, ax)
            else:
                pass

            #Add cartopy boundaries:
            wedgj_utils.add_geog_ref(self, ax)

            cbar = plt.colorbar(icecf, orientation = 'horizontal', label = 'Accreted Ice (in)', extendrect = True, aspect = 65, pad = 0)

            cbar.set_ticks((0, 0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0))
            plt.title(f'Total Accreted Ice (in)\n{domain} Region', loc = 'left', fontweight = 'bold', fontsize = 10)
            plt.title('Valid: {}\n{} HRRR F{:03d}'.format(ad+timedelta(hours=i),ad.strftime("%Y%m%d %HZ"),i), loc = 'right', fontsize = 10)
            plt.savefig('{}f{:03d}.png'.format(spath, i))
    
    except Exception as err:
        print(err)
        
  def hrrr_snow(self, spath = None, domain = 'CONUS', type = 'kuchera'):
 
    #Set up initial file and series of files:
    # Location of HRRR data:
    hrrr_url = "https://nomads.ncep.noaa.gov/pub/data/nccf/com/hrrr/prod/"

    # Build the HRRR urls
    urls = []
    date = datetime.utcnow()
    if (date.hour >= 21):
        date = date.replace(hour = 18)
    elif (date.hour >= 15):
        date = date.replace(hour = 12)
    elif (date.hour >= 9):
        date = date.replace(hour = 6)
    elif (date.hour >= 3):
        date = date.replace(hour = 0)
    else:
        date = date.replace(hour = 18)-timedelta(days=1)

    for i in range(49):
        urls.append(hrrr_url+"hrrr.{}/conus/hrrr.t{:02d}z.wrfprsf{:02d}.grib2".format(
            date.strftime("%Y%m%d"), date.hour, i))
            
    ### Loop over the run, downloading just the necessary fields:
    try:
        for i, url in enumerate(urls):
            # Download index file
            os.system("curl -o hrrr_index {}".format(url+".idx"))

            # Open index file to find relevant bytes
            f = open("hrrr_index", "r")
            lines = list(f)
            f.close()

            ### Do each variable in turn:
            data = {}
            for var in [("ASNOW", "surface"),  #in units of m
                         ("TMP", "2 m above ground"),
                         ("TMP", "850 mb"),
                         ("TMP", "700 mb"),
                         ("TMP", "500 mb")]: 

                # Check the index
                flag = False
                for line in lines:
                    # Check if var already found
                    if flag:
                        byte_end = line.split(":")[1]
                        break

                    # Locate variable
                    if ((var[0] in line) and (var[1] in line)):
                        byte_start = line.split(":")[1]
                        flag = True

                # Download the HRRR data
                os.system("curl -o hrrr_out -r {}-{} {}".format(byte_start, byte_end, url))

                # Grab the data
                grib = pygrib.open("hrrr_out")
                data[var[0]+var[1]] = grib[1].values
                lons = grib[1].longitudes.reshape(data[var[0]+var[1]].shape)
                lats = grib[1].latitudes.reshape(data[var[0]+var[1]].shape)
                vd = grib[1].validDate
                ad = grib[1].analDate
                grib.close()

            #Calculate 10:1 Ratio Snowfall Accumulation:
            snow = data["ASNOW"+"surface"] * 10 * 0.04 /0.01

            #Calculate Model-Ratio Snowfall Accumulation:
            model_snow = data["ASNOW"+"surface"] * 0.04  
 
            #Calculate Kuchera Method Snowfall Accumulation:
            temp = np.array([data["TMP"+"2 m above ground"],data["TMP"+"850 mb"],data["TMP"+"700 mb"],data["TMP"+"500 mb"]])
            
            kuchera = np.zeros(lons.shape)

            tmax = np.nanmax(temp, axis = 0)
                        
            for k in range(kuchera.shape[1]):
                for j in range(kuchera.shape[0]):
                    if tmax[j,k] > 271.16:
                        kuchera[j,k] = 12 + 2*(271.16 - tmax[j,k])
                    else:
                        kuchera[j,k] = 12 + (271.16 - tmax[j,k])
            
            kuchera = kuchera * ((snow)/10)
            
            kuchera[kuchera < 0.01] = np.nan        
            snow[snow < 0.01] = np.nan

            #Set dictionary to look up user input snow type for plotting:
            snow_type = {'kuchera':kuchera, '10:1': snow, 'model': model_snow}
            snow_type_title = {'kuchera': 'Kuchera Method', '10:1': '10:1', 'model': 'Model Ratio'}
            
            #Plot Snow Accumulation:
            figsize_table = wedgj_utils.figsize_table(self)

            #Make figure:
            fig, ax = plt.subplots(figsize = figsize_table[domain], subplot_kw = {'projection' : ccrs.crs.PlateCarree()})

            extent_table = wedgj_utils.extent_table(self)

            #Add cartopy boundaries::
            try:
              ax.set_extent(extent_table[domain])
            except:
              ax.set_extent(extent_table['CONUS'])
              print('Invalid Domain Input. Setting extent to CONUS.')
            
            snow_table = wedgj_utils.snow_cmap(self)
            
            barb_int = 16
            snowcf = ax.contourf(lons, lats, snow, cmap=snow_table['snow_cmap'], levels = snow_table['snow_clevs'], norm=mcolors.BoundaryNorm(snow_table['snow_clevs'], snow_table['snow_cmap'].N), transform = ccrs.crs.PlateCarree(), extend = 'max')

            #Add counties if not CONUS:
            if domain != 'CONUS':
              wedgj_utils.plot_counties(self, ax)
            
            #Add cities to state plots:
            if domain == 'Ohio':
                wedgj_utils.plot_oh_cities(self, ax)
            elif domain == 'Indiana':
                wedgj_utils.plot_in_cities(self, ax)
            elif domain == 'Alabama':
                wedgj_utils.plot_al_cities(self, ax)
            else:
                pass

            #Add cartopy boundaries:
            wedgj_utils.add_geog_ref(self, ax)
            
            cbar = plt.colorbar(snowcf, orientation = 'horizontal', label = 'Accumulated Snowfall (in)', extendrect = True, aspect = 65, pad = 0)
            cbar.set_ticks((0, 1, 3, 5, 8, 12, 18, 24, 36, 48, 60))
            plt.title(f'Model Ratio Accumulated Snowfall (in)\{domain} Region', loc = 'left', fontweight = 'bold', fontsize = 10)
            plt.title('Valid: {}\n{} HRRR F{:03d}'.format(ad+timedelta(hours=i),ad.strftime("%Y%m%d %HZ"),i), loc = 'right', fontsize = 10)
            plt.savefig('{}f{:03d}.png'.format(spath, i))
            
    except Exception as err:
        print(err)
