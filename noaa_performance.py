#Import necessary packages:
import numpy as np
import matplotlib.pyplot as plt
import cartopy as ccrs
import cartopy.feature as cfeature
from  datetime import datetime, timedelta
import cartopy.io.shapereader as shpreader
import geopandas as gpd 
import matplotlib.patches as mpatches
import pandas as pd
import warnings
from wedgj import wedgj_utils

###########################################
#                                         #
#            noaa_performance             #
#                                         #
###########################################

class noaa_performance:

  def __init__(self):
    self.date = datetime.utcnow()
    
###--------- NOAA Performance Function ---------###

  def noaa_performance(self, date = None, spath = None, domain = 'CONUS', report_type = 'All', warn_type = 'All', data = None, data_cint = None, data_levels = None):

    if date == None:
      date = self.date
      
    #Ignore download warnings for cartopy shapefiles:
    warnings.filterwarnings("ignore")


    ### Get Data:
    tornado_reports = pd.read_csv(f'https://spc.noaa.gov/climo/reports/{date.strftime("%y%m%d")}_rpts_torn.csv')
    wind_reports = pd.read_csv(f'https://spc.noaa.gov/climo/reports/{date.strftime("%y%m%d")}_rpts_wind.csv')
    hail_reports = pd.read_csv(f'https://spc.noaa.gov/climo/reports/{date.strftime("%y%m%d")}_rpts_hail.csv')

    link = "https://mesonet.agron.iastate.edu/pickup/wwa/{}_tsmf_sbw.zip".format(date.strftime("%Y"))
    warns = gpd.read_file(link)
    warns_gdf = gpd.GeoDataFrame(warns, geometry=warns['geometry'])
    warns_gdf.to_crs(4326)
    warns_gdf['ISSUED'] = warns_gdf['ISSUED'].astype('datetime64')
    
    
    #Refine sbw request to line up with 12-12 UTC SPC valid times for reports and outlooks:

    print(date)
    sbw_start = (date.replace(hour = 12) & date.replace(minute = 0))
    sbw_end = (date.replace(day = date.day + 1) & date.replace(hour = 11) & date.replace(minute = 59))
    print(sbw_start)
    print(sbw_end)
    #Define each type of warning:
    tor_warns = warns_gdf[(warns_gdf['PHENOM'] == 'TO') & (warns_gdf['STATUS'] == 'NEW') & (warns_gdf['ISSUED'] >= sbw_start.strftime('%Y%m%d%H%M')) & (warns_gdf['ISSUED'] <= sbw_end.strftime('%Y%m%d%H%M'))]
    flood_warns = warns_gdf[(warns_gdf['PHENOM'] == 'FF') & (warns_gdf['STATUS'] == 'NEW') & ((warns_gdf['ISSUED'] >= sbw_start.strftime('%Y%m%d%H%M')) & (warns_gdf['ISSUED'] <= sbw_end.strftime('%Y%m%d%H%M')))]
    svr_warns = warns_gdf[(warns_gdf['PHENOM'] == 'SV') & (warns_gdf['STATUS'] == 'NEW') & ((warns_gdf['ISSUED'] >= sbw_start.strftime('%Y%m%d%H%M')) & (warns_gdf['ISSUED'] <= sbw_end.strftime('%Y%m%d%H%M')))]

    # Build the SPC url:
    #SPC updates at 06, 13, 1630, 20, and 01 Z for Day 1 outlooks.
    date = date

    if (date.hour >= 20):
        date = date.replace(hour = 20)
        date = date.replace(minute = 0)
    elif ((date.hour >= 16) & (date.minute >=30)):
        date = date.replace(hour = 16)
        date = date.replace(minute = 30)
    elif (date.hour >= 13):
        date = date.replace(hour = 13)
        date = date.replace(minute = 0)
    elif (date.hour >= 6):
        date = date.replace(hour = 6)
        date = date.replace(minute = 0)
    else:
        date = date.replace(hour = 1)
        date = date.replace(minute = 0)

    #Link to the data and push into geodataframes:
    categorical = gpd.read_file('https://www.spc.noaa.gov/products/outlook/archive/{}/day1otlk_{}_{}_cat.lyr.geojson'.format(date.year, date.strftime("%Y%m%d"), date.strftime("%H%M")))
    cat_gdf = gpd.GeoDataFrame(categorical, geometry=categorical['geometry'], crs=4326)


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

    #Count total reports in domain:
    extent = extent_table[domain]
    torn_total = np.sum((tornado_reports['Lon'] > extent[0]) & (tornado_reports['Lon'] < extent[1]) & (tornado_reports['Lat'] > extent[2]) & (tornado_reports['Lat'] < extent[3]))
    wind_total = np.sum((wind_reports['Lon'] > extent[0]) & (wind_reports['Lon'] < extent[1]) & (wind_reports['Lat'] > extent[2]) & (wind_reports['Lat'] < extent[3]))
    hail_total = np.sum((hail_reports['Lon'] > extent[0]) & (hail_reports['Lon'] < extent[1]) & (hail_reports['Lat'] > extent[2]) & (hail_reports['Lat'] < extent[3]))

    #Determine centroids of warnings within the domain:
    tor_warn_lons = np.array(tor_warns['geometry'].centroid.x)
    tor_warn_lats = np.array(tor_warns['geometry'].centroid.y)
    svr_warn_lons = np.array(svr_warns['geometry'].centroid.x)
    svr_warn_lats = np.array(svr_warns['geometry'].centroid.y)
    fld_warn_lons = np.array(flood_warns['geometry'].centroid.x)
    fld_warn_lats = np.array(flood_warns['geometry'].centroid.y)
      
    if len(set(tor_warns['ISSUED'])) > 0: 
      for index,row in tor_warns.iterrows():
        tor_total = np.sum((tor_warn_lons > (extent[0])) & (tor_warn_lons < (extent[1])) & (tor_warn_lats > (extent[2])) & (tor_warn_lats < (extent[3])))
    else:
      tor_total = 0        
    if len(set(svr_warns['ISSUED'])) > 0: 
      for index,row in svr_warns.iterrows():
        svr_total = np.sum((svr_warn_lons > (extent[0])) & (svr_warn_lons < (extent[1])) & (svr_warn_lats > (extent[2])) & (svr_warn_lats < (extent[3])))
    else:
      svr_total = 0  
    if len(set(flood_warns['ISSUED'])) > 0: 
      for index,row in flood_warns.iterrows():
        fld_total = np.sum((fld_warn_lons > (extent[0])) & (fld_warn_lons < (extent[1])) & (fld_warn_lats > (extent[2])) & (fld_warn_lats < (extent[3])))    
    else:
      fld_total = 0  

    #Add sbw to legend:
    patch_tor = mpatches.Patch(edgecolor = 'black', label = f'Tornado Warning ({tor_total})', facecolor='tab:red', alpha = 0.5)
    patch_svr = mpatches.Patch(edgecolor = 'black', label = f'Severe Thunderstorm Warning ({svr_total})', facecolor='goldenrod', alpha = 0.5)
    patch_fld = mpatches.Patch(edgecolor= 'black', label = f'Flash Flood Warning ({fld_total})', facecolor='tab:green', alpha = 0.5)

    #Add reports to legend:
    patch_torn = mpatches.Patch(edgecolor = 'black', label = f'Tornado Reports ({torn_total})', facecolor='tab:red')
    patch_wind = mpatches.Patch(edgecolor = 'black', label = f'Wind Reports ({wind_total})', facecolor='tab:blue')
    patch_hail = mpatches.Patch(edgecolor= 'black', label = f'Hail Reports ({hail_total})', facecolor='tab:green')
   
    #Add categorical legend:
    patch_tstm  = mpatches.Patch(facecolor = 'None', label = 'TSTM', edgecolor='#55BB55')
    patch_mrgl = mpatches.Patch(facecolor = 'None', label = 'MRGL', edgecolor='#005500')
    patch_slgt = mpatches.Patch(facecolor = 'None', label = 'SLGT', edgecolor='#DDAA00')
    patch_enh = mpatches.Patch(facecolor = 'None', label = 'ENH', edgecolor='#FF6600')
    patch_mdt = mpatches.Patch(facecolor = 'None', label = 'MDT', edgecolor='#CC0000')
    patch_high = mpatches.Patch(facecolor = 'None', label = 'HIGH', edgecolor='#CC00CC')
    
    #Create legend:
    ax.legend(handles = [patch_tstm, patch_mrgl, patch_slgt, patch_enh, patch_mdt, patch_high, patch_torn, patch_wind, patch_hail, patch_tor, patch_svr, patch_fld], loc = (0.01,0.01), ncol = 4, fontsize = 8)

    ### Add data ###
    if data != None:
      ax.contourf(data['lons'], data['lats'], data['values'], cmap='turbo', extend = 'max', levels = data_levels)
      data_plot = ax.contour(data['lons'], data['lats'], data['values'], data_cint, colors = 'black', linewidths = 0.75, linestyles = '-')
      ax.clabel(data_plot, fontsize = 10, inline = 1, inline_spacing = 5, fmt = '%i', rightside_up = True, use_clabeltext = True)
      handles, labels = ax.get_legend_handles_labels()
      ax.legend(handles, labels, loc='lower right', ncol=1)

    
    ### Categorical SPC Outlook ###
    try:
      cat_gdf.loc[[0],'geometry'].plot(ax = ax, color = 'None', edgecolor = cat_gdf.loc[[0],'stroke'])
    except:
      pass
    try:
      cat_gdf.loc[[1],'geometry'].plot(ax = ax, color = 'None', edgecolor = cat_gdf.loc[[1],'stroke'])
    except:
      pass
    try:
      cat_gdf.loc[[2],'geometry'].plot(ax = ax, color = 'None', edgecolor = cat_gdf.loc[[2],'stroke'])
    except:
      pass
    try:
      cat_gdf.loc[[3],'geometry'].plot(ax = ax, color = 'None', edgecolor = cat_gdf.loc[[3],'stroke'])
    except:
      pass
    try:
      cat_gdf.loc[[4],'geometry'].plot(ax = ax, color = 'None', edgecolor = cat_gdf.loc[[4],'stroke'])
    except:
      pass
    try:
      cat_gdf.loc[[5],'geometry'].plot(ax = ax, color = 'None', edgecolor = cat_gdf.loc[[5],'stroke'])
    except:
      pass

    #Add warnings:
    if warn_type == 'All':  
      try:
        flood_warns['geometry'].plot(ax = ax, color = 'tab:green', edgecolor = 'darkgreen', alpha = 0.5)
      except:
        pass
      try:
        svr_warns['geometry'].plot(ax = ax, color = 'goldenrod', edgecolor = 'darkgoldenrod', alpha = 0.5)
      except:
        pass  
      try:
        tor_warns['geometry'].plot(ax = ax, color = 'tab:red', edgecolor = 'maroon', alpha = 0.5)
      except:
        pass
    elif warn_type == 'TOR':
      try:
        tor_warns['geometry'].plot(ax = ax, color = 'tab:red', edgecolor = 'maroon', alpha = 0.5)
      except:
        pass
    elif warn_type == 'SVR':
      try:
        svr_warns['geometry'].plot(ax = ax, color = 'goldenrod', edgecolor = 'darkgoldenrod', alpha = 0.5)
      except:
        pass  
    elif warn_type == 'FFW':
      try:
        flood_warns['geometry'].plot(ax = ax, color = 'tab:green', edgecolor = 'darkgreen', alpha = 0.5)
      except:
        pass
    else:
      print('Invalid warn_type input.')

    #Add reports:
    if report_type == 'All':
      try:
        ax.scatter(hail_reports['Lon'], hail_reports['Lat'], color = 'tab:green', linewidths = 0.5, edgecolor = 'black', s = 15, transform = ccrs.crs.PlateCarree(), label = 'Hail Reports', zorder = 10)
      except:
        pass
      try:
        ax.scatter(wind_reports['Lon'], wind_reports['Lat'], color = 'tab:blue', linewidths = 0.5, edgecolor = 'black', s = 15, transform = ccrs.crs.PlateCarree(), label = 'Wind Reports', zorder = 10)
      except:
        pass
      try:
        ax.scatter(tornado_reports['Lon'], tornado_reports['Lat'], color = 'tab:red', linewidths = 0.5, edgecolor = 'black', s = 15, transform = ccrs.crs.PlateCarree(), label = 'Tornado Reports', zorder = 10)
      except:
        pass
    elif report_type == 'Tornado':
      try:
        ax.scatter(tornado_reports['Lon'], tornado_reports['Lat'], color = 'tab:red', linewidths = 0.5, edgecolor = 'black', s = 15, transform = ccrs.crs.PlateCarree(), label = 'Tornado Reports', zorder = 10)
      except:
        pass
    elif report_type == 'Wind':
      try:
        ax.scatter(wind_reports['Lon'], wind_reports['Lat'], color = 'tab:blue', linewidths = 0.5, edgecolor = 'black', s = 15, transform = ccrs.crs.PlateCarree(), label = 'Wind Reports', zorder = 10)
      except:
        pass
    elif report_type == 'Hail':
      try:
        ax.scatter(hail_reports['Lon'], hail_reports['Lat'], color = 'tab:green', linewidths = 0.5, edgecolor = 'black', s = 15, transform = ccrs.crs.PlateCarree(), label = 'Hail Reports', zorder = 10)
      except:
        pass
    else:
      print('Invalid report_type input.')

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

    #Get end of valid time:
    date = date + timedelta(days=1)

    plt.tight_layout()
    plt.title('SPC/NWS Event Performance: {} Domain\n(Valid {} - {} [{}])'.format(domain, date.strftime("%Y%m%d 1200 UTC"), date.strftime("%Y%m%d 1159 UTC"), date.strftime("%H%M D1 SPC Outlook")), fontweight = 'bold', fontsize = 14)

    if spath != None:
      plt.savefig('{}/{}_{}_noaa_performance.png'.format(spath, date.strftime("%Y%m%d"), domain), dpi = 300)
    else:
      pass    
