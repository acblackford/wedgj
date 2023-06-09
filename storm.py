#Import necessary packages:
import numpy as np
import matplotlib.pyplot as plt
import cartopy as ccrs
import cartopy.feature as cfeature
from metpy.plots import USCOUNTIES
from  datetime import datetime, timedelta
import cartopy.io.shapereader as shpreader
import geopandas as gpd 
import matplotlib.patches as mpatches
import pandas as pd
import warnings

###########################################
#                                         #
#                 storm                   #
#                                         #
###########################################

class storm:

  def __init__(self):
    self.date = datetime.utcnow()
    
  #--------- Storm Reports Function ---------#

  def storm_reports(self, date = None, spath = None, domain = 'CONUS', report_type = 'All', data = None, data_cint = None, data_levels = None):

    if date == None:
      date = self.date
      
    #Ignore download warnings for cartopy shapefiles:
    warnings.filterwarnings("ignore")
    
    ### Get Data:
    tornado_reports = pd.read_csv(f'https://spc.noaa.gov/climo/reports/{date.strftime("%y%m%d")}_rpts_torn.csv')
    wind_reports = pd.read_csv(f'https://spc.noaa.gov/climo/reports/{date.strftime("%y%m%d")}_rpts_wind.csv')
    hail_reports = pd.read_csv(f'https://spc.noaa.gov/climo/reports/{date.strftime("%y%m%d")}_rpts_hail.csv')

    #Get figsizes for each oomain:
    figsize_table = {'Midwest': (8.5, 13), 'Northeast': (9, 12), 
              'Southeast': (10,13), 'TN Valley': (9,12), 'Southern Plains': (8,16), 
              'Northern Plains': (7,11), 'Northwest': (11,9),
              'Southwest': (11.5,11), 'Ohio': (7.5,12),
              'Indiana': (7.5,12.5), 'Alabama': (9,12),
              'CONUS': (15,13)}

    #Make figure:
    fig, ax = plt.subplots(figsize = figsize_table[domain], subplot_kw = {'projection' : ccrs.crs.PlateCarree()})

    #Determine extent:
    extent_table = {'Midwest': (-99.2, -78.27, 36.48, 49.64), 'Northeast': (-84.93, -66.21, 35.99, 47.68), 
                    'Southeast': (-95.39, -75.17, 24.50, 37.35), 'TN Valley': (-92, -81, 39.3, 33), 'Southern Plains': (-109.55, -90.34, 24.94, 40.38), 
                    'Northern Plains': (-106.71, -94.14, 39.15, 49.48), 'Northwest': (-125.37, -103.47, 40.75, 49.48),
                    'Southwest': (-125.21, -101.77, 30.97, 42.22), 'Ohio': (-85.14, -80.17, 37.92, 42.19),
                    'Indiana': (-88.97, -83.84, 37.32, 41.92), 'Alabama': (-89.65, -83.87, 29.64, 35.36),
                    'CONUS': (-127.0, -65.5, 23.0, 49.0)}

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

    #Add legend:
    patch_torn = mpatches.Patch(edgecolor = 'black', label = f'Tornado Reports ({torn_total})', facecolor='tab:red')
    patch_wind = mpatches.Patch(edgecolor = 'black', label = f'Wind Reports ({wind_total})', facecolor='tab:blue')
    patch_hail = mpatches.Patch(edgecolor= 'black', label = f'Hail Reports ({hail_total})', facecolor='tab:green')

    if report_type == 'All':
      ax.legend(handles = [patch_torn, patch_wind, patch_hail], loc = (0.01,0.01), ncol = 3, fontsize = 8)
    elif report_type == 'Tornado':
      ax.legend(handles = [patch_torn], loc = (0.01,0.01), fontsize = 8)
    elif report_type == 'Wind':
      ax.legend(handles = [patch_wind], loc = (0.01,0.01), fontsize = 8) 
    elif report_type == 'Hail':
      ax.legend(handles = [patch_hail], loc = (0.01,0.01), fontsize = 8)     

    ### Add data ###
    if data != None:
      ax.contourf(data['lons'], data['lats'], data['values'], cmap='turbo', extend = 'max', levels = data_levels)
      data_plot = ax.contour(data['lons'], data['lats'], data['values'], data_cint, colors = 'black', linewidths = 0.75, linestyles = '-')
      ax.clabel(data_plot, fontsize = 10, inline = 1, inline_spacing = 5, fmt = '%i', rightside_up = True, use_clabeltext = True)
      handles, labels = ax.get_legend_handles_labels()
      ax.legend(handles, labels, loc='lower right', ncol=1)

    #Add reports:
    if report_type == 'All':
      try:
        ax.scatter(hail_reports['Lon'], hail_reports['Lat'], color = 'tab:green', linewidths = 0.5, edgecolor = 'black', s = 20, transform = ccrs.crs.PlateCarree(), label = 'Hail Reports', zorder = 10)
      except:
        pass
      try:
        ax.scatter(wind_reports['Lon'], wind_reports['Lat'], color = 'tab:blue', linewidths = 0.5, edgecolor = 'black', s = 20, transform = ccrs.crs.PlateCarree(), label = 'Wind Reports', zorder = 10)
      except:
        pass
      try:
        ax.scatter(tornado_reports['Lon'], tornado_reports['Lat'], color = 'tab:red', linewidths = 0.5, edgecolor = 'black', s = 20, transform = ccrs.crs.PlateCarree(), label = 'Tornado Reports', zorder = 10)
      except:
        pass
    elif report_type == 'Tornado':
      try:
        ax.scatter(tornado_reports['Lon'], tornado_reports['Lat'], color = 'tab:red', linewidths = 0.5, edgecolor = 'black', s = 20, transform = ccrs.crs.PlateCarree(), label = 'Tornado Reports', zorder = 10)
      except:
        pass
    elif report_type == 'Wind':
      try:
        ax.scatter(wind_reports['Lon'], wind_reports['Lat'], color = 'tab:blue', linewidths = 0.5, edgecolor = 'black', s = 20, transform = ccrs.crs.PlateCarree(), label = 'Wind Reports', zorder = 10)
      except:
        pass
    elif report_type == 'Hail':
      try:
        ax.scatter(hail_reports['Lon'], hail_reports['Lat'], color = 'tab:green', linewidths = 0.5, edgecolor = 'black', s = 20, transform = ccrs.crs.PlateCarree(), label = 'Hail Reports', zorder = 10)
      except:
        pass
    else:
      print('Invalid report_type input.')

    #Add counties if not CONUS:
    if domain != 'CONUS':
      ax.add_feature(USCOUNTIES.with_scale('500k'), lw = 0.1, edgecolor = 'black') 
    
    #Add cities to state plots:
    if domain == 'Ohio':
      ax.add_feature(USCOUNTIES.with_scale('500k'), lw = 0.1, edgecolor = 'black')        
      Dayton = gpd.tools.geocode('Dayton, OH')
      Cincinnati = gpd.tools.geocode('Cincinnati, OH')
      Columbus = gpd.tools.geocode('Columbus, OH')
      Cleveland = gpd.tools.geocode('Cleveland, OH')
      Toledo = gpd.tools.geocode('Toledo, OH')
      Akron = gpd.tools.geocode('Akron, OH')
      oh_cities = [Dayton['geometry'][0], Cincinnati['geometry'][0], Columbus['geometry'][0], Cleveland['geometry'][0], Toledo['geometry'][0], Akron['geometry'][0]]
      oh_x = [point.x for point in oh_cities]
      oh_y = [point.y for point in oh_cities]

      oh_cities_labels = [Dayton['address'][0], Cincinnati['address'][0]]
      ax.scatter(oh_x, oh_y, color = 'None', edgecolor = 'black', s = 100, marker = 's', linewidths = 2, transform = ccrs.crs.PlateCarree(), label = oh_cities_labels, zorder = 10)
      #ax.annotate(oh_cities_labels, (oh_x, oh_y), textcoords="offset points", xytext=(3,3), ha='center')   


    shpfilename = shpreader.natural_earth(resolution='110m',
                                        category='cultural',
                                        name='admin_0_countries')
    reader = shpreader.Reader(shpfilename)
    countries = reader.records()

    for country in countries:
        if country.attributes['ADMIN'] != 'United States of America':
            ax.add_geometries([country.geometry], ccrs.crs.PlateCarree(),
                              facecolor=(1, 0.87, 0.75),
                              label=country.attributes['ADMIN'])
        else:
            pass

    ax.add_feature(cfeature.LAKES, facecolor = 'lightcyan', edgecolor = 'black', lw = 0.33)
    ax.add_feature(cfeature.STATES, lw = 0.5)
    ax.add_feature(cfeature.BORDERS, lw = 0.5)
    ax.add_feature(cfeature.OCEAN, facecolor = 'lightcyan', edgecolor = 'black', lw = 0.33)
    ax.add_feature(cfeature.COASTLINE, lw = 0.75)

    #Get end of valid time:
    end_date = date + timedelta(days=1)

    plt.tight_layout()
    plt.title('SPC Storm Reports: {} Domain\n(Valid {} - {})'.format(domain, date.strftime("%Y%m%d 1200 UTC"), end_date.strftime("%Y%m%d 1159 UTC")), fontweight = 'bold', fontsize = 14)

    if spath != None:
      plt.savefig('{}/{}_{}_storm_reports.png'.format(spath, date.strftime("%Y%m%d"), domain), dpi = 300)
    else:
      pass    

###---------Storm-Based Warning Function---------###

  def sbw(self, start_date = None, end_date = None, spath = None, domain = 'CONUS', warn_type = 'All'):

      if start_date == None:
        start_date = self.date - timedelta(days = 1, hours = 12)
      if end_date == None:
        end_date = self.date - timedelta(hours = 12)
      if start_date.year < 2002:
        raise ValueError('Input start_year must be 2002 or later.')

      #Ignore download warnings for cartopy shapefiles:
      warnings.filterwarnings("ignore")
      
      ### Get Data:
      
      #Check if selection is multi-year or single year:
      
      if end_date.year - start_date.year >= 1:
        years = np.arange(start_date.year, end_date.year + 1, 1)
        warns_gdf = gpd.GeoDataFrame()
        
        try:
           for year in years:
             link = "https://mesonet.agron.iastate.edu/pickup/wwa/{}_tsmf_sbw.zip".format(year)
             warns = gpd.read_file(link)
             warns_gdf_yrs = gpd.GeoDataFrame(warns, geometry=warns['geometry'])
             warns_gdf_yrs.to_crs(4326)
             warns_gdf_yrs['ISSUED'] = warns_gdf_yrs['ISSUED'].astype('datetime64')
             warns_gdf = pd.concat([warns_gdf_yrs, warns_gdf])
        except:
           raise ValueError('Multi-year selection failed.')
      else:
          link = "https://mesonet.agron.iastate.edu/pickup/wwa/{}_tsmf_sbw.zip".format(start_date.strftime("%Y"))
          warns = gpd.read_file(link)
          warns_gdf = gpd.GeoDataFrame(warns, geometry=warns['geometry'])
          warns_gdf.to_crs(4326)
          warns_gdf['ISSUED'] = warns_gdf['ISSUED'].astype('datetime64')
            
      #Define each type of warning:
      tor_warns = warns_gdf[(warns_gdf['PHENOM'] == 'TO') & (warns_gdf['STATUS'] == 'NEW') & (warns_gdf['ISSUED'] >= start_date.strftime('%Y%m%d%H%M')) & (warns_gdf['ISSUED'] <= end_date.strftime('%Y%m%d%H%M'))]
      flood_warns = warns_gdf[(warns_gdf['PHENOM'] == 'FF') & (warns_gdf['STATUS'] == 'NEW') & ((warns_gdf['ISSUED'] >= start_date.strftime('%Y%m%d%H%M')) & (warns_gdf['ISSUED'] <= end_date.strftime('%Y%m%d%H%M')))]
      svr_warns = warns_gdf[(warns_gdf['PHENOM'] == 'SV') & (warns_gdf['STATUS'] == 'NEW') & ((warns_gdf['ISSUED'] >= start_date.strftime('%Y%m%d%H%M')) & (warns_gdf['ISSUED'] <= end_date.strftime('%Y%m%d%H%M')))]

      #Get figsizes for each oomain:
      figsize_table = {'Midwest': (8.5, 13), 'Northeast': (9, 12), 
                'Southeast': (10,13), 'TN Valley': (9,12), 'Southern Plains': (8,16), 
                'Northern Plains': (7,11), 'Northwest': (11,9),
                'Southwest': (11.5,11), 'Ohio': (7.5,12),
                'Indiana': (7.5,12.5), 'Alabama': (9,12),
                'CONUS': (15,13)}

      #Make figure:
      fig, ax = plt.subplots(figsize = figsize_table[domain], subplot_kw = {'projection' : ccrs.crs.PlateCarree()})

      #Determine extent:
      extent_table = {'Midwest': (-99.2, -78.27, 36.48, 49.64), 'Northeast': (-84.93, -66.21, 35.99, 47.68), 
                      'Southeast': (-95.39, -75.17, 24.50, 37.35), 'TN Valley': (-92, -81, 39.3, 33), 'Southern Plains': (-109.55, -90.34, 24.94, 40.38), 
                      'Northern Plains': (-106.71, -94.14, 39.15, 49.48), 'Northwest': (-125.37, -103.47, 40.75, 49.48),
                      'Southwest': (-125.21, -101.77, 30.97, 42.22), 'Ohio': (-85.14, -80.17, 37.92, 42.19),
                      'Indiana': (-88.97, -83.84, 37.32, 41.92), 'Alabama': (-89.65, -83.87, 29.64, 35.36),
                      'CONUS': (-127.0, -65.5, 23.0, 49.0)}

      #Add cartopy boundaries::
      try:
        ax.set_extent(extent_table[domain])
      except:
        ax.set_extent(extent_table['CONUS'])
        print('Invalid Domain Input. Setting extent to CONUS.')

      #Count total warnings in domain:
      extent = extent_table[domain]

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

      #Add legend:
      patch_tor = mpatches.Patch(edgecolor = 'black', label = f'Tornado Warning ({tor_total})', facecolor='tab:red')
      patch_svr = mpatches.Patch(edgecolor = 'black', label = f'Severe Thunderstorm Warning ({svr_total})', facecolor='goldenrod')
      patch_fld = mpatches.Patch(edgecolor= 'black', label = f'Flash Flood Warning ({fld_total})', facecolor='tab:green')

      if warn_type == 'All':
        ax.legend(handles = [patch_tor, patch_svr, patch_fld], loc = (0.01,0.01), ncol = 3, fontsize = 8)
      elif warn_type == 'TOR':
        ax.legend(handles = [patch_tor], loc = (0.01,0.01), fontsize = 8)
      elif warn_type == 'SVR':
        ax.legend(handles = [patch_svr], loc = (0.01,0.01), fontsize = 8) 
      elif warn_type == 'FFW':
        ax.legend(handles = [patch_fld], loc = (0.01,0.01), fontsize = 8)     

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

      #Add counties if not CONUS:
      if domain != 'CONUS':
        ax.add_feature(USCOUNTIES.with_scale('500k'), lw = 0.1, edgecolor = 'black') 
      
      #Add cities to state plots:
      if domain == 'Ohio':
        ax.add_feature(USCOUNTIES.with_scale('500k'), lw = 0.1, edgecolor = 'black')        
        Dayton = gpd.tools.geocode('Dayton, OH')
        Cincinnati = gpd.tools.geocode('Cincinnati, OH')
        Columbus = gpd.tools.geocode('Columbus, OH')
        Cleveland = gpd.tools.geocode('Cleveland, OH')
        Toledo = gpd.tools.geocode('Toledo, OH')
        Akron = gpd.tools.geocode('Akron, OH')
        oh_cities = [Dayton['geometry'][0], Cincinnati['geometry'][0], Columbus['geometry'][0], Cleveland['geometry'][0], Toledo['geometry'][0], Akron['geometry'][0]]
        oh_x = [point.x for point in oh_cities]
        oh_y = [point.y for point in oh_cities]

        oh_cities_labels = [Dayton['address'][0], Cincinnati['address'][0], Columbus['address'][0], Cleveland['address'][0], Toledo['address'][0], Akron['address'][0]]
        cities = ax.scatter(oh_x, oh_y, color = 'None', edgecolor = 'black', s = 100, marker = 's', linewidths = 2, transform = ccrs.crs.PlateCarree(), zorder = 10)
  
        for i in enumerate(oh_x):
          ax.text(oh_x[i] + 0.01, oh_y[i] + 0.01, oh_cities_labels[i], horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
          
      shpfilename = shpreader.natural_earth(resolution='110m',
                                          category='cultural',
                                          name='admin_0_countries')
      reader = shpreader.Reader(shpfilename)
      countries = reader.records()

      for country in countries:
          if country.attributes['ADMIN'] != 'United States of America':
              ax.add_geometries([country.geometry], ccrs.crs.PlateCarree(),
                                facecolor=(1, 0.87, 0.75),
                                label=country.attributes['ADMIN'])
          else:
              pass

      ax.add_feature(cfeature.LAKES, facecolor = 'lightcyan', edgecolor = 'black', lw = 0.33)
      ax.add_feature(cfeature.STATES, lw = 0.5)
      ax.add_feature(cfeature.BORDERS, lw = 0.5)
      ax.add_feature(cfeature.OCEAN, facecolor = 'lightcyan', edgecolor = 'black', lw = 0.33)
      ax.add_feature(cfeature.COASTLINE, lw = 0.75)

      plt.tight_layout()
      plt.title('NWS Storm-Based Warnings: {} Domain\n(Valid {} - {})'.format(domain, start_date.strftime("%Y%m%d %H%M UTC"), end_date.strftime("%Y%m%d %H%M UTC")), fontweight = 'bold', fontsize = 14)

      if spath != None:
        plt.savefig('{}/{}_to_{}_{}_{}_warnings.png'.format(spath, start_date.strftime("%Y%m%d_%H%M"), end_date.strftime("%Y%m%d_%H%M"), domain, warn_type), dpi = 300)
      else:
        pass       


  ###---------Tornado Path Function---------###


  def tor_plot(self, start_date, end_date, spath = None, domain = 'CONUS', tor_type = 'Both', rating = 'All'):

      if start_date.year < 1950:
        raise ValueError('Input start_year must be 1950 or later.')
      if end_date.year > 2022:
        raise ValueError('Input end_year must be 2022 or earlier.')

      #Ignore download warnings for cartopy shapefiles:
      warnings.filterwarnings("ignore")
        
      ### Get Data:
      tor_paths = "https://www.spc.noaa.gov/gis/svrgis/zipped/1950-2022-torn-aspath.zip!1950-2022-torn-aspath/1950-2022-torn-aspath.shp"
      tor_pts = "https://www.spc.noaa.gov/gis/svrgis/zipped/1950-2022-torn-initpoint.zip!1950-2022-torn-initpoint/1950-2022-torn-initpoint.shp"
      tor_paths = gpd.read_file(tor_paths)
      tor_pts = gpd.read_file(tor_pts)
      tor_paths_gdf = gpd.GeoDataFrame(tor_paths, geometry=tor_paths['geometry'])
      tor_paths_gdf.to_crs(4326)
      tor_pts_gdf = gpd.GeoDataFrame(tor_pts, geometry=tor_pts['geometry'])
      tor_pts_gdf.to_crs(4326)
      
      tor_paths_gdf['date'] = tor_paths_gdf['date'].astype('datetime64')
      tor_pts_gdf['date'] = tor_pts_gdf['date'].astype('datetime64')

      #Define each rating:
      #Paths:
      tor_paths_UNK = tor_paths_gdf[(tor_paths_gdf['mag'] == -9) & (tor_paths_gdf['date'] >= start_date.strftime('%Y-%m-%d')) & (tor_paths_gdf['date'] <= end_date.strftime('%Y-%m-%d'))]
      tor_paths_F0 = tor_paths_gdf[(tor_paths_gdf['mag'] == 0) & (tor_paths_gdf['date'] >= start_date.strftime('%Y-%m-%d')) & (tor_paths_gdf['date'] <= end_date.strftime('%Y-%m-%d'))]
      tor_paths_F1 = tor_paths_gdf[(tor_paths_gdf['mag'] == 1) & (tor_paths_gdf['date'] >= start_date.strftime('%Y-%m-%d')) & (tor_paths_gdf['date'] <= end_date.strftime('%Y-%m-%d'))]
      tor_paths_F2 = tor_paths_gdf[(tor_paths_gdf['mag'] == 2) & (tor_paths_gdf['date'] >= start_date.strftime('%Y-%m-%d')) & (tor_paths_gdf['date'] <= end_date.strftime('%Y-%m-%d'))]
      tor_paths_F3 = tor_paths_gdf[(tor_paths_gdf['mag'] == 3) & (tor_paths_gdf['date'] >= start_date.strftime('%Y-%m-%d')) & (tor_paths_gdf['date'] <= end_date.strftime('%Y-%m-%d'))]
      tor_paths_F4 = tor_paths_gdf[(tor_paths_gdf['mag'] == 4) & (tor_paths_gdf['date'] >= start_date.strftime('%Y-%m-%d')) & (tor_paths_gdf['date'] <= end_date.strftime('%Y-%m-%d'))]
      tor_paths_F5 = tor_paths_gdf[(tor_paths_gdf['mag'] == 5) & (tor_paths_gdf['date'] >= start_date.strftime('%Y-%m-%d')) & (tor_paths_gdf['date'] <= end_date.strftime('%Y-%m-%d'))]
      #Points:
      tor_points_UNK = tor_pts_gdf[(tor_pts_gdf['mag'] == -9) & (tor_pts_gdf['date'] >= start_date.strftime('%Y-%m-%d')) & (tor_pts_gdf['date'] <= end_date.strftime('%Y-%m-%d'))]
      tor_points_F0 = tor_pts_gdf[(tor_pts_gdf['mag'] == 0) & (tor_pts_gdf['date'] >= start_date.strftime('%Y-%m-%d')) & (tor_pts_gdf['date'] <= end_date.strftime('%Y-%m-%d'))]
      tor_points_F1 = tor_pts_gdf[(tor_pts_gdf['mag'] == 1) & (tor_pts_gdf['date'] >= start_date.strftime('%Y-%m-%d')) & (tor_pts_gdf['date'] <= end_date.strftime('%Y-%m-%d'))]
      tor_points_F2 = tor_pts_gdf[(tor_pts_gdf['mag'] == 2) & (tor_pts_gdf['date'] >= start_date.strftime('%Y-%m-%d')) & (tor_pts_gdf['date'] <= end_date.strftime('%Y-%m-%d'))]
      tor_points_F3 = tor_pts_gdf[(tor_pts_gdf['mag'] == 3) & (tor_pts_gdf['date'] >= start_date.strftime('%Y-%m-%d')) & (tor_pts_gdf['date'] <= end_date.strftime('%Y-%m-%d'))]
      tor_points_F4 = tor_pts_gdf[(tor_pts_gdf['mag'] == 4) & (tor_pts_gdf['date'] >= start_date.strftime('%Y-%m-%d')) & (tor_pts_gdf['date'] <= end_date.strftime('%Y-%m-%d'))]
      tor_points_F5 = tor_pts_gdf[(tor_pts_gdf['mag'] == 5) & (tor_pts_gdf['date'] >= start_date.strftime('%Y-%m-%d')) & (tor_pts_gdf['date'] <= end_date.strftime('%Y-%m-%d'))]

      #Get figsizes for each domain:
      figsize_table = {'Midwest': (8.5, 13), 'Northeast': (9, 12), 
                'Southeast': (10,13), 'TN Valley': (9,12), 'Southern Plains': (8,16), 
                'Northern Plains': (7,11), 'Northwest': (11,9),
                'Southwest': (11.5,11), 'Ohio': (7.5,12),
                'Indiana': (7.5,12.5), 'Alabama': (9,12),
                'CONUS': (15,13)}

      #Make figure:
      fig, ax = plt.subplots(figsize = figsize_table[domain], subplot_kw = {'projection' : ccrs.crs.PlateCarree()})

      #Determine extent:
      extent_table = {'Midwest': (-99.2, -78.27, 36.48, 49.64), 'Northeast': (-84.93, -66.21, 35.99, 47.68), 
                      'Southeast': (-95.39, -75.17, 24.50, 37.35), 'TN Valley': (-92, -81, 39.3, 33), 'Southern Plains': (-109.55, -90.34, 24.94, 40.38), 
                      'Northern Plains': (-106.71, -94.14, 39.15, 49.48), 'Northwest': (-125.37, -103.47, 40.75, 49.48),
                      'Southwest': (-125.21, -101.77, 30.97, 42.22), 'Ohio': (-85.14, -80.17, 37.92, 42.19),
                      'Indiana': (-88.97, -83.84, 37.32, 41.92), 'Alabama': (-89.65, -83.87, 29.64, 35.36),
                      'CONUS': (-127.0, -65.5, 23.0, 49.0)}

      #Add cartopy boundaries::
      try:
        ax.set_extent(extent_table[domain])
      except:
        ax.set_extent(extent_table['CONUS'])
        print('Invalid Domain Input. Setting extent to CONUS.')

      ###Count total tornadoes in domain by rating:
      extent = extent_table[domain]

      #Determine centroids of tornadoes within the domain:
      tor_paths_UNK_lons = np.array(tor_paths_UNK['geometry'].centroid.x)
      tor_paths_UNK_lats = np.array(tor_paths_UNK['geometry'].centroid.y)      
      tor_paths_F0_lons = np.array(tor_paths_F0['geometry'].centroid.x)
      tor_paths_F0_lats = np.array(tor_paths_F0['geometry'].centroid.y)
      tor_paths_F1_lons = np.array(tor_paths_F1['geometry'].centroid.x)
      tor_paths_F1_lats = np.array(tor_paths_F1['geometry'].centroid.y)
      tor_paths_F2_lons = np.array(tor_paths_F2['geometry'].centroid.x)
      tor_paths_F2_lats = np.array(tor_paths_F2['geometry'].centroid.y)
      tor_paths_F3_lons = np.array(tor_paths_F3['geometry'].centroid.x)
      tor_paths_F3_lats = np.array(tor_paths_F3['geometry'].centroid.y)
      tor_paths_F4_lons = np.array(tor_paths_F4['geometry'].centroid.x)
      tor_paths_F4_lats = np.array(tor_paths_F4['geometry'].centroid.y)
      tor_paths_F5_lons = np.array(tor_paths_F5['geometry'].centroid.x)
      tor_paths_F5_lats = np.array(tor_paths_F5['geometry'].centroid.y)

      if len(set(tor_paths_UNK['date'])) > 0:
        for index,row in tor_paths_UNK.iterrows():
          UNK_total = np.sum((tor_paths_UNK_lons > (extent[0])) & (tor_paths_UNK_lons < (extent[1])) & (tor_paths_UNK_lats > (extent[2])) & (tor_paths_UNK_lats < (extent[3])))
      else:
        UNK_total = 0
      if len(set(tor_paths_F0['date'])) > 0:        
        for index,row in tor_paths_F0.iterrows():
          F0_total = np.sum((tor_paths_F0_lons > (extent[0])) & (tor_paths_F0_lons < (extent[1])) & (tor_paths_F0_lats > (extent[2])) & (tor_paths_F0_lats < (extent[3])))
      else:
        F0_total = 0
      if len(set(tor_paths_F1['date'])) > 0:    
        for index,row in tor_paths_F1.iterrows():
          F1_total = np.sum((tor_paths_F1_lons > (extent[0])) & (tor_paths_F1_lons < (extent[1])) & (tor_paths_F1_lats > (extent[2])) & (tor_paths_F1_lats < (extent[3])))
      else:
        F1_total = 0
      if len(set(tor_paths_F2['date'])) > 0:    
        for index,row in tor_paths_F2.iterrows():
         F2_total = np.sum((tor_paths_F2_lons > (extent[0])) & (tor_paths_F2_lons < (extent[1])) & (tor_paths_F2_lats > (extent[2])) & (tor_paths_F2_lats < (extent[3])))  
      else:
        F2_total = 0
      if len(set(tor_paths_F3['date'])) > 0:    
        for index,row in tor_paths_F3.iterrows():
          F3_total = np.sum((tor_paths_F3_lons > (extent[0])) & (tor_paths_F3_lons < (extent[1])) & (tor_paths_F3_lats > (extent[2])) & (tor_paths_F3_lats < (extent[3])))
      else:
        F3_total = 0
      if len(set(tor_paths_F4['date'])) > 0:    
        for index,row in tor_paths_F4.iterrows():
          F4_total = np.sum((tor_paths_F4_lons > (extent[0])) & (tor_paths_F4_lons < (extent[1])) & (tor_paths_F4_lats > (extent[2])) & (tor_paths_F4_lats < (extent[3])))
      else:
        F4_total = 0
      if len(set(tor_paths_F5['date'])) > 0:           
        for index,row in tor_paths_F5.iterrows():
          F5_total = np.sum((tor_paths_F5_lons.isnull() > (extent[0])) & (tor_paths_F5_lons.isnull() < (extent[1])) & (tor_paths_F5_lats.isnull() > (extent[2])) & (tor_paths_F5_lats.isnull() < (extent[3]))) 
      else:
        F5_total = 0

      #Get total tornado count:
      tor_total_array = [UNK_total, F0_total, F1_total, F2_total, F3_total, F4_total, F5_total]
      tor_total = np.sum(tor_total_array)   

      #Set colors:
      tor_colors = {'UNK': 'lightgrey', 'F0': 'deepskyblue', 'F1': 'lime', 'F2': 'gold', 'F3': 'darkorange', 'F4': 'firebrick', 'F5': 'deeppink'}

      #Add tornadoes:
      if tor_type == 'Both':
        if rating == 'All':  
          try:
            tor_paths_UNK['geometry'].plot(ax = ax, color = tor_colors['UNK'])
            ax.scatter(tor_points_UNK['slon'], tor_points_UNK['slat'], color = tor_colors['UNK'], linewidths = 0.5, edgecolor = 'black', s = 20, marker = 'v', transform = ccrs.crs.PlateCarree(), zorder = 10)
          except:
            pass          
          try:
            tor_paths_F0['geometry'].plot(ax = ax, color = tor_colors['F0'])
            ax.scatter(tor_points_F0['slon'], tor_points_F0['slat'], color = tor_colors['F0'], linewidths = 0.5, edgecolor = 'black', s = 20, marker = 'v', transform = ccrs.crs.PlateCarree(), zorder = 10)
          except:
            pass
          try:
            tor_paths_F1['geometry'].plot(ax = ax, color = tor_colors['F1'])
            ax.scatter(tor_points_F1['slon'], tor_points_F1['slat'], color = tor_colors['F1'], linewidths = 0.5, edgecolor = 'black', s = 20, marker = 'v', transform = ccrs.crs.PlateCarree(), zorder = 10)
          except:
            pass
          try:
            tor_paths_F2['geometry'].plot(ax = ax, color = tor_colors['F2'])
            ax.scatter(tor_points_F2['slon'], tor_points_F2['slat'], color = tor_colors['F2'], linewidths = 0.5, edgecolor = 'black', s = 20, marker = 'v', transform = ccrs.crs.PlateCarree(), zorder = 10)
          except:
            pass
          try:
            tor_paths_F3['geometry'].plot(ax = ax, color = tor_colors['F3'])
            ax.scatter(tor_points_F3['slon'], tor_points_F3['slat'], color = tor_colors['F3'], linewidths = 0.5, edgecolor = 'black', s = 20, marker = 'v', transform = ccrs.crs.PlateCarree(), zorder = 10)
          except:
            pass
          try:
            tor_paths_F4['geometry'].plot(ax = ax, color = tor_colors['F4'])
            ax.scatter(tor_points_F4['slon'], tor_points_F4['slat'], color = tor_colors['F4'], linewidths = 0.5, edgecolor = 'black', s = 20, marker = 'v', transform = ccrs.crs.PlateCarree(), zorder = 10)
          except:
            pass
          try:
            tor_paths_F5['geometry'].plot(ax = ax, color = tor_colors['F5'])
            ax.scatter(tor_points_F5['slon'], tor_points_F5['slat'], color = tor_colors['F5'], linewidths = 0.5, edgecolor = 'black', s = 20, marker = 'v', transform = ccrs.crs.PlateCarree(), zorder = 10)
          except:
            pass
        elif rating == 'Significant':        
          try:
            tor_paths_F2['geometry'].plot(ax = ax, color = tor_colors['F2'])
            tor_points_F2['geometry'].plot(ax = ax, color = tor_colors['F2'], edgecolor = 'black')
          except:
            pass
          try:
            tor_paths_F3['geometry'].plot(ax = ax, color = tor_colors['F3'])
            tor_points_F3['geometry'].plot(ax = ax, color = tor_colors['F3'], edgecolor = 'black')
          except:
            pass
          try:
            tor_paths_F4['geometry'].plot(ax = ax, color = tor_colors['F4'])
            tor_points_F4['geometry'].plot(ax = ax, color = tor_colors['F4'], edgecolor = 'black')
          except:
            pass
          try:
            tor_paths_F5['geometry'].plot(ax = ax, color = tor_colors['F5'])
            tor_points_F5['geometry'].plot(ax = ax, color = tor_colors['F5'], edgecolor = 'black')
          except:
            pass

        elif rating == 'Violent':        
          try:
            tor_paths_F4['geometry'].plot(ax = ax, color = tor_colors['F4'])
            tor_points_F4['geometry'].plot(ax = ax, color = tor_colors['F4'], edgecolor = 'black')
          except:
            pass
          try:
            tor_paths_F5['geometry'].plot(ax = ax, color = tor_colors['F5'])
            tor_points_F5['geometry'].plot(ax = ax, color = tor_colors['F5'], edgecolor = 'black')
          except:
            pass
        elif rating =='UNK':
          try:
            tor_paths_UNK['geometry'].plot(ax = ax, color = tor_colors['UNK'])
            tor_points_UNK['geometry'].plot(ax = ax, color = tor_colors['UNK'], edgecolor = 'black')
          except:
            pass
        elif rating =='0':
          try:
            tor_paths_F0['geometry'].plot(ax = ax, color = tor_colors['F0'])
            tor_points_F0['geometry'].plot(ax = ax, color = tor_colors['F0'], edgecolor = 'black')
          except:
            pass
        elif rating =='1':
          try:
            tor_paths_F1['geometry'].plot(ax = ax, color = tor_colors['F1'])
            tor_points_F1['geometry'].plot(ax = ax, color = tor_colors['F1'], edgecolor = 'black')
          except:
            pass
        elif rating =='2':
          try:
            tor_paths_F2['geometry'].plot(ax = ax, color = tor_colors['F2'])
            tor_points_F2['geometry'].plot(ax = ax, color = tor_colors['F2'], edgecolor = 'black')
          except:
            pass
        elif rating =='3':
          try:
            tor_paths_F3['geometry'].plot(ax = ax, color = tor_colors['F3'])
            tor_points_F3['geometry'].plot(ax = ax, color = tor_colors['F3'], edgecolor = 'black')
          except:
            pass
        elif rating =='4':
          try:
            tor_paths_F4['geometry'].plot(ax = ax, color = tor_colors['F4'])
            tor_points_F4['geometry'].plot(ax = ax, color = tor_colors['F4'], edgecolor = 'black')
          except:
            pass
        elif rating =='5':
          try:
            tor_paths_F5['geometry'].plot(ax = ax, color = tor_colors['F5'])
            tor_points_F5['geometry'].plot(ax = ax, color = tor_colors['F5'], edgecolor = 'black')
          except:
            pass          

      elif tor_type == 'Paths':
        if rating == 'All':  
          try:
            tor_paths_UNK['geometry'].plot(ax = ax, color = tor_colors['UNK'])
          except:
            pass
          try:
            tor_paths_F0['geometry'].plot(ax = ax, color = tor_colors['F0'])
          except:
            pass
          try:
            tor_paths_F1['geometry'].plot(ax = ax, color = tor_colors['F1'])
          except:
            pass
          try:
            tor_paths_F2['geometry'].plot(ax = ax, color = tor_colors['F2'])
          except:
            pass
          try:
            tor_paths_F3['geometry'].plot(ax = ax, color = tor_colors['F3'])
          except:
            pass
          try:
            tor_paths_F4['geometry'].plot(ax = ax, color = tor_colors['F4'])
          except:
            pass
          try:
            tor_paths_F5['geometry'].plot(ax = ax, color = tor_colors['F5'])
          except:
            pass
        elif rating == 'Significant':        
          try:
            tor_paths_F2['geometry'].plot(ax = ax, color = tor_colors['F2'])
          except:
            pass
          try:
            tor_paths_F3['geometry'].plot(ax = ax, color = tor_colors['F3'])
          except:
            pass
          try:
            tor_paths_F4['geometry'].plot(ax = ax, color = tor_colors['F4'])
          except:
            pass
          try:
            tor_paths_F5['geometry'].plot(ax = ax, color = tor_colors['F5'])
          except:
            pass
        elif rating == 'Violent':        
          try:
            tor_paths_F4['geometry'].plot(ax = ax, color = tor_colors['F4'])
          except:
            pass
          try:
            tor_paths_F5['geometry'].plot(ax = ax, color = tor_colors['F5'])
          except:
            pass
        elif rating =='UNK':
          try:
            tor_paths_UNK['geometry'].plot(ax = ax, color = tor_colors['UNK'])
          except:
            pass        
        elif rating =='0':
          try:
            tor_paths_F0['geometry'].plot(ax = ax, color = tor_colors['F0'])
          except:
            pass
        elif rating =='1':
          try:
            tor_paths_F1['geometry'].plot(ax = ax, color = tor_colors['F1'])
          except:
            pass
        elif rating =='2':
          try:
            tor_paths_F2['geometry'].plot(ax = ax, color = tor_colors['F2'])
          except:
            pass
        elif rating =='3':
          try:
            tor_paths_F3['geometry'].plot(ax = ax, color = tor_colors['F3'])
          except:
            pass
        elif rating =='4':
          try:
            tor_paths_F4['geometry'].plot(ax = ax, color = tor_colors['F4'])
          except:
            pass
        elif rating =='5':
          try:
            tor_paths_F5['geometry'].plot(ax = ax, color = tor_colors['F5'])
          except:
            pass          

      elif tor_type == 'Points':
        if rating == 'All':  
          try:
            ax.scatter(tor_points_UNK['slon'], tor_points_UNK['slat'], color = tor_colors['UNK'], linewidths = 0.5, edgecolor = 'black', s = 20, marker = 'v', transform = ccrs.crs.PlateCarree(), zorder = 10)
          except:
            pass          
          try:
            ax.scatter(tor_points_F0['slon'], tor_points_F0['slat'], color = tor_colors['F0'], linewidths = 0.5, edgecolor = 'black', s = 20, marker = 'v', transform = ccrs.crs.PlateCarree(), zorder = 10)
          except:
            pass
          try:
            ax.scatter(tor_points_F1['slon'], tor_points_F1['slat'], color = tor_colors['F1'], linewidths = 0.5, edgecolor = 'black', s = 20, marker = 'v', transform = ccrs.crs.PlateCarree(), zorder = 10)
          except:
            pass
          try:
            ax.scatter(tor_points_F2['slon'], tor_points_F2['slat'], color = tor_colors['F2'], linewidths = 0.5, edgecolor = 'black', s = 20, marker = 'v', transform = ccrs.crs.PlateCarree(), zorder = 10)
          except:
            pass
          try:
            ax.scatter(tor_points_F3['slon'], tor_points_F3['slat'], color = tor_colors['F3'], linewidths = 0.5, edgecolor = 'black', s = 20, marker = 'v', transform = ccrs.crs.PlateCarree(), zorder = 10)
          except:
            pass
          try:
            ax.scatter(tor_points_F4['slon'], tor_points_F4['slat'], color = tor_colors['F4'], linewidths = 0.5, edgecolor = 'black', s = 20, marker = 'v', transform = ccrs.crs.PlateCarree(), zorder = 10)
          except:
            pass
          try:
            ax.scatter(tor_points_F5['slon'], tor_points_F5['slat'], color = tor_colors['F5'], linewidths = 0.5, edgecolor = 'black', s = 20, marker = 'v', transform = ccrs.crs.PlateCarree(), zorder = 10)
          except:
            pass
        elif rating == 'Significant':        
          try:
            ax.scatter(tor_points_F2['slon'], tor_points_F2['slat'], color = tor_colors['F2'], linewidths = 0.5, edgecolor = 'black', s = 20, marker = 'v', transform = ccrs.crs.PlateCarree(), zorder = 10)
          except:
            pass
          try:
            ax.scatter(tor_points_F3['slon'], tor_points_F3['slat'], color = tor_colors['F3'], linewidths = 0.5, edgecolor = 'black', s = 20, marker = 'v', transform = ccrs.crs.PlateCarree(), zorder = 10)
          except:
            pass
          try:
            ax.scatter(tor_points_F4['slon'], tor_points_F4['slat'], color = tor_colors['F4'], linewidths = 0.5, edgecolor = 'black', s = 20, marker = 'v', transform = ccrs.crs.PlateCarree(), zorder = 10)
          except:
            pass
          try:
            ax.scatter(tor_points_F5['slon'], tor_points_F5['slat'], color = tor_colors['F5'], linewidths = 0.5, edgecolor = 'black', s = 20, marker = 'v', transform = ccrs.crs.PlateCarree(), zorder = 10)
          except:
            pass
        elif rating == 'Violent':        
          try:
            ax.scatter(tor_points_F4['slon'], tor_points_F4['slat'], color = tor_colors['F4'], linewidths = 0.5, edgecolor = 'black', s = 20, marker = 'v', transform = ccrs.crs.PlateCarree(), zorder = 10)
          except:
            pass
          try:
            ax.scatter(tor_points_F5['slon'], tor_points_F5['slat'], color = tor_colors['F5'], linewidths = 0.5, edgecolor = 'black', s = 20, marker = 'v', transform = ccrs.crs.PlateCarree(), zorder = 10)
          except:
            pass
        elif rating =='UNK':
          try:
            ax.scatter(tor_points_UNK['slon'], tor_points_UNK['slat'], color = tor_colors['UNK'], linewidths = 0.5, edgecolor = 'black', s = 20, marker = 'v', transform = ccrs.crs.PlateCarree(), zorder = 10)
          except:
            pass
        elif rating =='0':
          try:
            ax.scatter(tor_points_F0['slon'], tor_points_F0['slat'], color = tor_colors['F0'], linewidths = 0.5, edgecolor = 'black', s = 20, marker = 'v', transform = ccrs.crs.PlateCarree(), zorder = 10)
          except:
            pass
        elif rating =='1':
          try:
            ax.scatter(tor_points_F1['slon'], tor_points_F1['slat'], color = tor_colors['F1'], linewidths = 0.5, edgecolor = 'black', s = 20, marker = 'v', transform = ccrs.crs.PlateCarree(), zorder = 10)
          except:
            pass
        elif rating =='2':
          try:
            ax.scatter(tor_points_F2['slon'], tor_points_F2['slat'], color = tor_colors['F2'], linewidths = 0.5, edgecolor = 'black', s = 20, marker = 'v', transform = ccrs.crs.PlateCarree(), zorder = 10)
          except:
            pass
        elif rating =='3':
          try:
            ax.scatter(tor_points_F3['slon'], tor_points_F3['slat'], color = tor_colors['F3'], linewidths = 0.5, edgecolor = 'black', s = 20, marker = 'v', transform = ccrs.crs.PlateCarree(), zorder = 10)
          except:
            pass
        elif rating =='4':
          try:
            ax.scatter(tor_points_F4['slon'], tor_points_F4['slat'], color = tor_colors['F4'], linewidths = 0.5, edgecolor = 'black', s = 20, marker = 'v', transform = ccrs.crs.PlateCarree(), zorder = 10)
          except:
            pass
        elif rating =='5':
          try:
            ax.scatter(tor_points_F5['slon'], tor_points_F5['slat'], color = tor_colors['F5'], linewidths = 0.5, edgecolor = 'black', s = 20, marker = 'v', transform = ccrs.crs.PlateCarree(), zorder = 10)
          except:
            pass      

      else:
        print('Invalid tor_type input.')

      #Add legend:
      patch_UNK = mpatches.Patch(edgecolor = 'black', label = f'F/EF UNK ({UNK_total})', facecolor=tor_colors['UNK'])
      patch_F0 = mpatches.Patch(edgecolor = 'black', label = f'F/EF 0 ({F0_total})', facecolor=tor_colors['F0'])
      patch_F1 = mpatches.Patch(edgecolor = 'black', label = f'F/EF 1 ({F1_total})', facecolor=tor_colors['F1'])
      patch_F2 = mpatches.Patch(edgecolor= 'black', label = f'F/EF 2 ({F2_total})', facecolor=tor_colors['F2'])
      patch_F3 = mpatches.Patch(edgecolor = 'black', label = f'F/EF 3 ({F3_total})', facecolor=tor_colors['F3'])
      patch_F4 = mpatches.Patch(edgecolor = 'black', label = f'F/EF 4 ({F4_total})', facecolor=tor_colors['F4'])
      patch_F5 = mpatches.Patch(edgecolor= 'black', label = f'F/EF 5 ({F5_total})', facecolor=tor_colors['F5'])
      patch_TOT = mpatches.Patch(edgecolor= 'None', label = f'Total: {tor_total}', facecolor='None')

      ax.legend(handles = [patch_UNK, patch_F0, patch_F1, patch_F2, patch_F3, patch_F4, patch_F5, patch_TOT], loc = (0.01,0.01), ncol = 3, fontsize = 8) 

      #Add counties if not CONUS:
      if domain != 'CONUS':
        ax.add_feature(USCOUNTIES.with_scale('500k'), lw = 0.1, edgecolor = 'black') 
      
      shpfilename = shpreader.natural_earth(resolution='110m',
                                          category='cultural',
                                          name='admin_0_countries')
      reader = shpreader.Reader(shpfilename)
      countries = reader.records()

      for country in countries:
          if country.attributes['ADMIN'] != 'United States of America':
              ax.add_geometries([country.geometry], ccrs.crs.PlateCarree(),
                                facecolor=(1, 0.87, 0.75),
                                label=country.attributes['ADMIN'])
          else:
              pass

      ax.add_feature(cfeature.LAKES, facecolor = 'lightcyan', edgecolor = 'black', lw = 0.33)
      ax.add_feature(cfeature.STATES, lw = 0.5)
      ax.add_feature(cfeature.BORDERS, lw = 0.5)
      ax.add_feature(cfeature.OCEAN, facecolor = 'lightcyan', edgecolor = 'black', lw = 0.33)
      ax.add_feature(cfeature.COASTLINE, lw = 0.75)

      plt.tight_layout()
      plt.title('Confirmed Tornadoes (NWS/SPC): {} Domain\n(Valid {} - {})'.format(domain, start_date.strftime("%Y%m%d"), end_date.strftime("%Y%m%d")), fontweight = 'bold', fontsize = 14)

      if spath != None:
        plt.savefig('{}/{}_to_{}_{}_tornadoes.png'.format(spath, start_date.strftime("%Y%m%d_%H%M"), end_date.strftime("%Y%m%d_%H%M"), domain), dpi = 300)
      else:
        pass             
