#Import necessary packages:
import matplotlib.pyplot as plt
import cartopy as ccrs
import cartopy.feature as cfeature
from  datetime import datetime
import cartopy.io.shapereader as shpreader
import geopandas as gpd 
import matplotlib.patches as mpatches
import warnings
from wedgj import wedgj_utils

###########################################
#                                         #
#                spc_plot                 #
#                                         #
###########################################

class spc_plot:

  def __init__(self):
    self.date = datetime.utcnow()

  #--------- Day 1 and 2 Outlook Function ---------#

  def day1_2_outlook(self, date = None, spath = None, domain = 'CONUS', outlook_day = 'day1'):

    if date == None:
      date = self.date
    
    #Set dictionary for outlook day label:
    ### BEGIN OPTIONS ###
    var = outlook_day
    ### END OPTIONS ###

    var_label = {'day1':'Day 1', 'day2':'Day 2'}

    #Ignore download warnings for cartopy shapefiles:
    warnings.filterwarnings("ignore")
    
    ### Get Data ###

    # Build the SPC url:
    #SPC updates at 06, 13, 1630, 20, and 01 Z for Day 1 outlooks.
    date = date
    if outlook_day == 'day1':
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

    elif outlook_day == 'day2':
      if ((date.hour >= 17) & (date.minute >= 30)):
          date = date.replace(hour = 17)
          date = date.replace(minute = 30)        
      else:
          date = date.replace(hour = 6)
          date = date.replace(minute = 0)   
    else:
      raise ValueError('Invalid outlook_day passed.')


    #Link to the data and push into geodataframes:
    categorical = gpd.read_file('https://www.spc.noaa.gov/products/outlook/archive/{}/{}otlk_{}_{}_cat.lyr.geojson'.format(date.year, outlook_day, date.strftime("%Y%m%d"), date.strftime("%H%M")))
    cat_gdf = gpd.GeoDataFrame(categorical, geometry=categorical['geometry'], crs=4326)
    tor = gpd.read_file('https://www.spc.noaa.gov/products/outlook/archive/{}/{}otlk_{}_{}_torn.lyr.geojson'.format(date.year, outlook_day, date.strftime("%Y%m%d"), date.strftime("%H%M")))
    tor_gdf = gpd.GeoDataFrame(tor, geometry=tor['geometry'], crs=4326)
    wind = gpd.read_file('https://www.spc.noaa.gov/products/outlook/archive/{}/{}otlk_{}_{}_wind.lyr.geojson'.format(date.year, outlook_day, date.strftime("%Y%m%d"), date.strftime("%H%M")))
    wind_gdf = gpd.GeoDataFrame(wind, geometry=wind['geometry'], crs=4326)
    hail = gpd.read_file('https://www.spc.noaa.gov/products/outlook/archive/{}/{}otlk_{}_{}_hail.lyr.geojson'.format(date.year, outlook_day, date.strftime("%Y%m%d"), date.strftime("%H%M")))
    hail_gdf = gpd.GeoDataFrame(hail, geometry=hail['geometry'], crs=4326)

    #Remove signficant layer from gdfs if they exist, then grab the significant polygons as single layers:
    if 'SIGN' in list(tor_gdf['LABEL']):
      tor_gdf = tor_gdf[:-1]
    if 'SIGN' in list(wind_gdf['LABEL']):
      wind_gdf = wind_gdf[:-1]
    if 'SIGN' in list(hail_gdf['LABEL']):
      hail_gdf = hail_gdf[:-1]

    sigtor = gpd.read_file('https://www.spc.noaa.gov/products/outlook/archive/{}/{}otlk_{}_{}_sigtorn.lyr.geojson'.format(date.year, outlook_day, date.strftime("%Y%m%d"), date.strftime("%H%M")))
    sigtor_gdf = gpd.GeoDataFrame(sigtor, geometry=sigtor['geometry'], crs=4326)
    sigwind = gpd.read_file('https://www.spc.noaa.gov/products/outlook/archive/{}/{}otlk_{}_{}_sigwind.lyr.geojson'.format(date.year, outlook_day, date.strftime("%Y%m%d"), date.strftime("%H%M")))
    sigwind_gdf = gpd.GeoDataFrame(sigwind, geometry=sigwind['geometry'], crs=4326)
    sighail = gpd.read_file('https://www.spc.noaa.gov/products/outlook/archive/{}/{}otlk_{}_{}_sighail.lyr.geojson'.format(date.year, outlook_day, date.strftime("%Y%m%d"), date.strftime("%H%M")))
    sighail_gdf = gpd.GeoDataFrame(sighail, geometry=sighail['geometry'], crs=4326)

    figsize_table = wedgj_utils.figsize_table(self)

    #Plot the figure:
    fig, ax = plt.subplots(figsize = (16,12), ncols = 2, nrows = 2, subplot_kw = {'projection' : ccrs.crs.PlateCarree()})

    ### Categorical ###
    try:
      cat_gdf.loc[[0],'geometry'].plot(ax = ax[0,0], color = cat_gdf.loc[[0],'fill'], edgecolor = cat_gdf.loc[[0],'stroke'])
    except:
      pass
    try:
      cat_gdf.loc[[1],'geometry'].plot(ax = ax[0,0], color = cat_gdf.loc[[1],'fill'], edgecolor = cat_gdf.loc[[1],'stroke'])
    except:
      pass
    try:
      cat_gdf.loc[[2],'geometry'].plot(ax = ax[0,0], color = cat_gdf.loc[[2],'fill'], edgecolor = cat_gdf.loc[[2],'stroke'])
    except:
      pass
    try:
      cat_gdf.loc[[3],'geometry'].plot(ax = ax[0,0], color = cat_gdf.loc[[3],'fill'], edgecolor = cat_gdf.loc[[3],'stroke'])
    except:
      pass
    try:
      cat_gdf.loc[[4],'geometry'].plot(ax = ax[0,0], color = cat_gdf.loc[[4],'fill'], edgecolor = cat_gdf.loc[[4],'stroke'])
    except:
      pass
    try:
      cat_gdf.loc[[5],'geometry'].plot(ax = ax[0,0], color = cat_gdf.loc[[5],'fill'], edgecolor = cat_gdf.loc[[5],'stroke'])
    except:
      pass

    #Add categorical legend:
    patch_tstm  = mpatches.Patch(facecolor = '#C1E9C1', label = 'TSTM', edgecolor='#55BB55')
    patch_mrgl = mpatches.Patch(facecolor = '#66A366', label = 'MRGL', edgecolor='#005500')
    patch_slgt = mpatches.Patch(facecolor = '#FFE066', label = 'SLGT', edgecolor='#DDAA00')
    patch_enh = mpatches.Patch(facecolor = '#FFA366', label = 'ENH', edgecolor='#FF6600')
    patch_mdt = mpatches.Patch(facecolor = '#E06666', label = 'MDT', edgecolor='#CC0000')
    patch_high = mpatches.Patch(facecolor = '#EE99EE', label = 'HIGH', edgecolor='#CC00CC')
    ax[0,0].legend(handles = [patch_tstm, patch_mrgl, patch_slgt, patch_enh, patch_mdt, patch_high], loc = (0.01,0.01), ncol = 3, fontsize = 8)

    ### Tornado ###
    try:
      tor_gdf.loc[[0],'geometry'].plot(ax = ax[0,1], color = tor_gdf.loc[[0],'fill'], edgecolor = tor_gdf.loc[[0],'stroke'])
    except:
      pass
    try:
      tor_gdf.loc[[1],'geometry'].plot(ax = ax[0,1], color = tor_gdf.loc[[1],'fill'], edgecolor = tor_gdf.loc[[1],'stroke'])
    except:
      pass
    try:
      tor_gdf.loc[[2],'geometry'].plot(ax = ax[0,1], color = tor_gdf.loc[[2],'fill'], edgecolor = tor_gdf.loc[[2],'stroke'])
    except:
      pass
    try:
      tor_gdf.loc[[3],'geometry'].plot(ax = ax[0,1], color = tor_gdf.loc[[3],'fill'], edgecolor = tor_gdf.loc[[3],'stroke'])
    except:
      pass
    try:
      tor_gdf.loc[[4],'geometry'].plot(ax = ax[0,1], color = tor_gdf.loc[[4],'fill'], edgecolor = tor_gdf.loc[[4],'stroke'])
    except:
      pass
    try:
      tor_gdf.loc[[5],'geometry'].plot(ax = ax[0,1], color = tor_gdf.loc[[5],'fill'], edgecolor = tor_gdf.loc[[5],'stroke'])
    except:
      pass
    try:
      tor_gdf.loc[[6],'geometry'].plot(ax = ax[0,1], color = tor_gdf.loc[[6],'fill'], edgecolor = tor_gdf.loc[[6],'stroke'])
    except:
      pass
    try:
      sigtor_gdf.loc[[0],'geometry'].plot(ax = ax[0,1], color = 'None', edgecolor = sigtor_gdf.loc[[0],'stroke'], hatch = '/')
    except:
      pass

    #Add tornado legend:
    patch_tor2  = mpatches.Patch(facecolor = '#66A366', label = '2%', edgecolor='#005500')
    patch_tor5 = mpatches.Patch(facecolor = '#9d4e15', label = '5%', edgecolor='#70380f')
    patch_tor10 = mpatches.Patch(facecolor = '#FFE066', label = '10%', edgecolor='#DDAA00')
    patch_tor15 = mpatches.Patch(facecolor = '#E06666', label = '15%', edgecolor='#CC0000')
    patch_tor30 = mpatches.Patch(facecolor = '#EE99EE', label = '30%', edgecolor='#CC00CC')
    patch_tor45 = mpatches.Patch(facecolor = '#C895F6', label = '45%', edgecolor='#912CEE')
    patch_tor60 = mpatches.Patch(facecolor = '#348EE8', label = '60%', edgecolor='#104E8B')
    patch_sigtor = mpatches.Patch(facecolor = '#000000', label = 'SIG', edgecolor='#000000')
    ax[0,1].legend(handles = [patch_tor2, patch_tor5, patch_tor10, patch_tor15, patch_tor30, patch_tor45, patch_tor60, patch_sigtor], loc = (0.01,0.01), ncol = 4, fontsize = 8)

    ### Wind ###
    try:
      wind_gdf.loc[[0],'geometry'].plot(ax = ax[1,0], color = wind_gdf.loc[[0],'fill'], edgecolor = wind_gdf.loc[[0],'stroke'])
    except:
      pass
    try:
      wind_gdf.loc[[1],'geometry'].plot(ax = ax[1,0], color = wind_gdf.loc[[1],'fill'], edgecolor = wind_gdf.loc[[1],'stroke'])
    except:
      pass
    try:
      wind_gdf.loc[[2],'geometry'].plot(ax = ax[1,0], color = wind_gdf.loc[[2],'fill'], edgecolor = wind_gdf.loc[[2],'stroke'])
    except:
      pass
    try:
      wind_gdf.loc[[3],'geometry'].plot(ax = ax[1,0], color = wind_gdf.loc[[3],'fill'], edgecolor = wind_gdf.loc[[3],'stroke'])
    except:
      pass
    try:
      wind_gdf.loc[[4],'geometry'].plot(ax = ax[1,0], color = wind_gdf.loc[[4],'fill'], edgecolor = wind_gdf.loc[[4],'stroke'])
    except:
      pass
    try:
      sigwind_gdf.loc[[0],'geometry'].plot(ax = ax[1,0], color = 'None', edgecolor = sigwind_gdf.loc[[0],'stroke'], hatch = '/')
    except:
      pass

    #Add wind legend:
    patch_wind5  = mpatches.Patch(facecolor = '#9d4e15', label = '5%', edgecolor='#70380f')
    patch_wind15 = mpatches.Patch(facecolor = '#FFE066', label = '15%', edgecolor='#DDAA00')
    patch_wind30 = mpatches.Patch(facecolor = '#E06666', label = '30%', edgecolor='#CC0000')
    patch_wind45 = mpatches.Patch(facecolor = '#EE99EE', label = '45%', edgecolor='#CC00CC')
    patch_wind60 = mpatches.Patch(facecolor = '#C895F6', label = '60%', edgecolor='#912CEE')
    patch_sigwind = mpatches.Patch(facecolor = '#000000', label = 'SIG', edgecolor='#000000')
    ax[1,0].legend(handles = [patch_wind5, patch_wind15, patch_wind30, patch_wind45, patch_wind60, patch_sigwind], loc = (0.01,0.01), ncol = 3, fontsize = 8)

    ### Hail ###
    try:
      hail_gdf.loc[[0],'geometry'].plot(ax = ax[1,1], color = hail_gdf.loc[[0],'fill'], edgecolor = hail_gdf.loc[[0],'stroke'])
    except:
      pass
    try:
      hail_gdf.loc[[1],'geometry'].plot(ax = ax[1,1], color = hail_gdf.loc[[1],'fill'], edgecolor = hail_gdf.loc[[1],'stroke'])
    except:
      pass
    try:
      hail_gdf.loc[[2],'geometry'].plot(ax = ax[1,1], color = hail_gdf.loc[[2],'fill'], edgecolor = hail_gdf.loc[[2],'stroke'])
    except:
      pass
    try:
      hail_gdf.loc[[3],'geometry'].plot(ax = ax[1,1], color = hail_gdf.loc[[3],'fill'], edgecolor = hail_gdf.loc[[3],'stroke'])
    except:
      pass
    try:
      hail_gdf.loc[[4],'geometry'].plot(ax = ax[1,1], color = hail_gdf.loc[[4],'fill'], edgecolor = hail_gdf.loc[[4],'stroke'])
    except:
      pass
    try:
      sighail_gdf.loc[[0],'geometry'].plot(ax = ax[1,1], color = 'None', edgecolor = sighail_gdf.loc[[0],'stroke'], hatch = '/')
    except:
      pass

    #Add hail legend (same colormap as wind):
    ax[1,1].legend(handles = [patch_wind5, patch_wind15, patch_wind30, patch_wind45, patch_wind60, patch_sigwind], loc = (0.01,0.01), ncol = 3, fontsize = 8)


    plot_loc = [ax[0,0], ax[0,1], ax[1,0], ax[1,1]]

    #Set titles:
    plot_loc[0].set_title('Categorical', fontsize = 14)
    plot_loc[1].set_title('Tornado', fontsize = 14)
    plot_loc[2].set_title('Wind', fontsize = 14)
    plot_loc[3].set_title('Hail', fontsize = 14)
    plt.suptitle('SPC {} Outlook: {} Domain (Valid {})'.format(var_label[f'{var}'], domain, date.strftime("%Y%m%d %H%M UTC")), fontweight = 'bold', fontsize = 18)
    
    #Add cartopy boundaries:
    for ax in plot_loc:
      #Determine extent:
      extent_table = wedgj_utils.extent_table(self)

      #Add cartopy boundaries::
      try:
        ax.set_extent(extent_table[domain])
      except:
        ax.set_extent(extent_table['CONUS'])
        print('Invalid Domain Input. Setting extent to CONUS.')
      #Add counties if not CONUS:
      if domain != 'CONUS':
        wedgj_utils.plot_counties(self, ax)

      #Add cartopy boundaries:
      wedgj_utils.add_geog_ref(self, ax)

    plt.tight_layout()

    if spath != None:
     plt.savefig('{}/{}_{}_4panel.png'.format(spath, date.strftime("%Y%m%d_%H%MUTC"), var), dpi = 300)
    else:
      pass

  #--------- Day 3 Outlook Function ---------#

  def day3_outlook(self, date = None, spath = None, domain = 'CONUS'):

    if date == None:
      date = self.date
      
    #Ignore download warnings for cartopy shapefiles:
    warnings.filterwarnings("ignore")
    
    ### Get Data ###

    # Build the SPC url:
    #SPC updates at 0730 Z or 0830 Z for Day 3 outlooks, dependent on Daylight Savings.

    #Link to the data and push into geodataframes:
    try:
      categorical = gpd.read_file('https://www.spc.noaa.gov/products/outlook/archive/{}/day3otlk_{}_0730_cat.lyr.geojson'.format(date.year, date.strftime("%Y%m%d")))
      cat_gdf = gpd.GeoDataFrame(categorical, geometry=categorical['geometry'], crs=4326)
      prob = gpd.read_file('https://www.spc.noaa.gov/products/outlook/archive/{}/day3otlk_{}_0730_prob.lyr.geojson'.format(date.year, date.strftime("%Y%m%d")))
      prob_gdf = gpd.GeoDataFrame(prob, geometry=prob['geometry'], crs=4326)
      #If significant layer exists, remove it and grab single significant layer link:
      if 'SIGN' in list(prob_gdf['LABEL']):
        prob_gdf = prob_gdf[:-1]
      sigprob = gpd.read_file('https://www.spc.noaa.gov/products/outlook/archive/{}/day3otlk_{}_0730_sigprob.lyr.geojson'.format(date.year, date.strftime("%Y%m%d")))
      sigprob_gdf = gpd.GeoDataFrame(sigprob, geometry=sigprob['geometry'], crs=4326)

    except:
      try:
        categorical = gpd.read_file('https://www.spc.noaa.gov/products/outlook/archive/{}/day3otlk_{}_0830_cat.lyr.geojson'.format(date.year, date.strftime("%Y%m%d")))
        cat_gdf = gpd.GeoDataFrame(categorical, geometry=categorical['geometry'], crs=4326)
        prob = gpd.read_file('https://www.spc.noaa.gov/products/outlook/archive/{}/day3otlk_{}_0830_prob.lyr.geojson'.format(date.year, date.strftime("%Y%m%d")))
        prob_gdf = gpd.GeoDataFrame(prob, geometry=prob['geometry'], crs=4326)
        #If significant layer exists, remove it and grab single significant layer link:
        if 'SIGN' in list(prob_gdf['LABEL']):
          prob_gdf = prob_gdf[:-1]
        sigprob = gpd.read_file('https://www.spc.noaa.gov/products/outlook/archive/{}/day3otlk_{}_0830_sigprob.lyr.geojson'.format(date.year, date.strftime("%Y%m%d")))
        sigprob_gdf = gpd.GeoDataFrame(sigprob, geometry=sigprob['geometry'], crs=4326)
      except:
        raise ValueError('Invalid date. Request failed.')

    figsize_table = wedgj_utils.figsize_table(self)

    #Plot the figure:
    fig, (ax0, ax1) = plt.subplots(figsize = ((figsize_table[domain][0]*2), figsize_table[domain][1]), ncols = 2, nrows = 1, subplot_kw = {'projection' : ccrs.crs.PlateCarree()})

    ### Categorical ###
    try:
      cat_gdf.loc[[0],'geometry'].plot(ax = ax0, color = cat_gdf.loc[[0],'fill'], edgecolor = cat_gdf.loc[[0],'stroke'])
    except:
      pass
    try:
      cat_gdf.loc[[1],'geometry'].plot(ax = ax0, color = cat_gdf.loc[[1],'fill'], edgecolor = cat_gdf.loc[[1],'stroke'])
    except:
      pass
    try:
      cat_gdf.loc[[2],'geometry'].plot(ax = ax0, color = cat_gdf.loc[[2],'fill'], edgecolor = cat_gdf.loc[[2],'stroke'])
    except:
      pass
    try:
      cat_gdf.loc[[3],'geometry'].plot(ax = ax0, color = cat_gdf.loc[[3],'fill'], edgecolor = cat_gdf.loc[[3],'stroke'])
    except:
      pass
    try:
      cat_gdf.loc[[4],'geometry'].plot(ax = ax0, color = cat_gdf.loc[[4],'fill'], edgecolor = cat_gdf.loc[[4],'stroke'])
    except:
      pass
    try:
      cat_gdf.loc[[5],'geometry'].plot(ax = ax0, color = cat_gdf.loc[[5],'fill'], edgecolor = cat_gdf.loc[[5],'stroke'])
    except:
      pass

    #Add categorical legend:
    patch_tstm  = mpatches.Patch(facecolor = '#C1E9C1', label = 'TSTM', edgecolor='#55BB55')
    patch_mrgl = mpatches.Patch(facecolor = '#66A366', label = 'MRGL', edgecolor='#005500')
    patch_slgt = mpatches.Patch(facecolor = '#FFE066', label = 'SLGT', edgecolor='#DDAA00')
    patch_enh = mpatches.Patch(facecolor = '#FFA366', label = 'ENH', edgecolor='#FF6600')
    patch_mdt = mpatches.Patch(facecolor = '#E06666', label = 'MDT', edgecolor='#CC0000')
    patch_high = mpatches.Patch(facecolor = '#EE99EE', label = 'HIGH', edgecolor='#CC00CC')
    ax0.legend(handles = [patch_tstm, patch_mrgl, patch_slgt, patch_enh, patch_mdt, patch_high], loc = (0.01,0.01), ncol = 3, fontsize = 8)

    ### Probabilistic ###
    try:
      prob_gdf.loc[[0],'geometry'].plot(ax = ax1, color = prob_gdf.loc[[0],'fill'], edgecolor = prob_gdf.loc[[0],'stroke'])
    except:
      pass
    try:
      prob_gdf.loc[[1],'geometry'].plot(ax = ax1, color = prob_gdf.loc[[1],'fill'], edgecolor = prob_gdf.loc[[1],'stroke'])
    except:
      pass
    try:
      prob_gdf.loc[[2],'geometry'].plot(ax = ax1, color = prob_gdf.loc[[2],'fill'], edgecolor = prob_gdf.loc[[2],'stroke'])
    except:
      pass
    try:
      prob_gdf.loc[[3],'geometry'].plot(ax = ax1, color = prob_gdf.loc[[3],'fill'], edgecolor = prob_gdf.loc[[3],'stroke'])
    except:
      pass
    try:
      prob_gdf.loc[[4],'geometry'].plot(ax = ax1, color = prob_gdf.loc[[4],'fill'], edgecolor = prob_gdf.loc[[4],'stroke'])
    except:
      pass
    try:
      sigprob_gdf.loc[[0],'geometry'].plot(ax = ax1, color = 'None', edgecolor = sigprob_gdf.loc[[0],'stroke'], hatch = '/')
    except:
      pass

    #Add probabilistic legend:
    patch_prob5  = mpatches.Patch(facecolor = '#9d4e15', label = '5%', edgecolor='#70380f')
    patch_prob15 = mpatches.Patch(facecolor = '#FFE066', label = '15%', edgecolor='#DDAA00')
    patch_prob30 = mpatches.Patch(facecolor = '#E06666', label = '30%', edgecolor='#CC0000')
    patch_prob45 = mpatches.Patch(facecolor = '#EE99EE', label = '45%', edgecolor='#CC00CC')
    patch_prob60 = mpatches.Patch(facecolor = '#C895F6', label = '60%', edgecolor='#912CEE')
    patch_sigprob = mpatches.Patch(facecolor = '#000000', label = 'SIG', edgecolor='#000000')
    ax1.legend(handles = [patch_prob5, patch_prob15, patch_prob30, patch_prob45, patch_prob60, patch_sigprob], loc = (0.01,0.01), ncol = 3, fontsize = 8)


    plot_loc = [ax0, ax1]

    #Set titles:
    plot_loc[0].set_title('Categorical', fontsize = 14)
    plot_loc[1].set_title('Probabilistic', fontsize = 14)

    #Add cartopy boundaries:
    for ax in plot_loc:
      #Determine extent:
      extent_table = wedgj_utils.extent_table(self)

      #Add cartopy boundaries::
      try:
        ax.set_extent(extent_table[domain])
      except:
        ax.set_extent(extent_table['CONUS'])
        print('Invalid Domain Input. Setting extent to CONUS.')
        
      #Add counties if not CONUS:
      if domain != 'CONUS':
        wedgj_utils.plot_counties(self, ax)
      
      #Add cartopy boundaries:
      wedgj_utils.add_geog_ref(self, ax)

    plt.tight_layout()
    ax0.text(-0.01, 1.1, 'SPC Day 3 Outlook: {} Domain (Valid {})'.format(domain, date.strftime("%Y%m%d")), fontweight = 'bold', fontsize = 18, ha='center', va='center', transform=ax.transAxes)

    if spath != None:
      plt.savefig('{}/{}_{}_D3_4panel.png'.format(spath, date.strftime("%Y%m%d"), domain), dpi = 300)
    else:
      pass


  #--------- Days 4-8 Outlook Function ---------#


  def day4_8_outlook(self, date = None, spath = None, domain = 'CONUS'):

    if date == None:
      date = self.date

    #Ignore download warnings for cartopy shapefiles:
    warnings.filterwarnings("ignore")
      
    ### Get Data:
    d4 = gpd.read_file('https://www.spc.noaa.gov/products/exper/day4-8/archive/{}/day4prob_{}.lyr.geojson'.format(date.year, date.strftime("%Y%m%d")))
    d4_gdf = gpd.GeoDataFrame(d4, geometry=d4['geometry'], crs=4326)
    d5 = gpd.read_file('https://www.spc.noaa.gov/products/exper/day4-8/archive/{}/day5prob_{}.lyr.geojson'.format(date.year, date.strftime("%Y%m%d")))
    d5_gdf = gpd.GeoDataFrame(d5, geometry=d5['geometry'], crs=4326)
    d6 = gpd.read_file('https://www.spc.noaa.gov/products/exper/day4-8/archive/{}/day6prob_{}.lyr.geojson'.format(date.year, date.strftime("%Y%m%d")))
    d6_gdf = gpd.GeoDataFrame(d6, geometry=d6['geometry'], crs=4326)
    d7 = gpd.read_file('https://www.spc.noaa.gov/products/exper/day4-8/archive/{}/day7prob_{}.lyr.geojson'.format(date.year, date.strftime("%Y%m%d")))
    d7_gdf = gpd.GeoDataFrame(d7, geometry=d7['geometry'], crs=4326)
    d8 = gpd.read_file('https://www.spc.noaa.gov/products/exper/day4-8/archive/{}/day8prob_{}.lyr.geojson'.format(date.year, date.strftime("%Y%m%d")))
    d8_gdf = gpd.GeoDataFrame(d8, geometry=d8['geometry'], crs=4326)

    #Plot the figure:
    fig, ax = plt.subplots(figsize = (16,8), ncols = 3, nrows = 2, subplot_kw = {'projection' : ccrs.crs.PlateCarree()})

    ### Day 4 ###
    try:
      d4_gdf.loc[[0],'geometry'].plot(ax = ax[0,0], color = d4_gdf.loc[[0],'fill'], edgecolor = d4_gdf.loc[[0],'stroke'])
    except:
      pass
    ### Day 5 ###
    try:
      d5_gdf.loc[[0],'geometry'].plot(ax = ax[0,1], color = d5_gdf.loc[[0],'fill'], edgecolor = d5_gdf.loc[[0],'stroke'])
    except:
      pass
    ### Day 6 ###
    try:
      d6_gdf.loc[[0],'geometry'].plot(ax = ax[0,2], color = d6_gdf.loc[[0],'fill'], edgecolor = d6_gdf.loc[[0],'stroke'])
    except:
      pass
    ### Day 7 ###
    try:
      d7_gdf.loc[[0],'geometry'].plot(ax = ax[1,0], color = d7_gdf.loc[[0],'fill'], edgecolor = d7_gdf.loc[[0],'stroke'])
    except:
      pass
    ### Day 8 ###
    try:
      d8_gdf.loc[[0],'geometry'].plot(ax = ax[1,1], color = d8_gdf.loc[[0],'fill'], edgecolor = d8_gdf.loc[[0],'stroke'])
    except:
      pass

    #Add probabilistic legend:
    patch15 = mpatches.Patch(facecolor = '#FFE066', label = '15%', edgecolor='#DDAA00')
    patch30 = mpatches.Patch(facecolor = '#FFA366', label = '30%', edgecolor='#FF6600')
    ax[1,2].legend(handles = [patch15, patch30], loc = (0.25, 0.5), ncol = 2, fontsize = 14)

    plot_loc = [ax[0,0], ax[0,1], ax[0,2], ax[1,0], ax[1,1]]
    #Turn off extra axis:
    ax[1,2].set_axis_off()

    #Set titles:
    plot_loc[0].set_title('Day 4', fontweight = 'bold')
    plot_loc[1].set_title('SPC Day 4-8 Outlook: {} Domain (Valid {})'.format(domain, date.strftime("%Y%m%d"))+'\nDay 5', fontweight = 'bold')
    plot_loc[2].set_title('Day 6', fontweight = 'bold')
    plot_loc[3].set_title('Day 7', fontweight = 'bold')
    plot_loc[4].set_title('Day 8', fontweight = 'bold')

    #Add cartopy boundaries:
    for ax in plot_loc:
      #Determine extent:
      extent_table = wedgj_utils.extent_table(self)

      #Set aspect ratio:
      ax.set_aspect(1.1)

      #Add cartopy boundaries::
      try:
        ax.set_extent(extent_table[domain])
      except:
        ax.set_extent(extent_table['CONUS'])
        print('Invalid Domain Input. Setting extent to CONUS.')
      #Add counties if not CONUS:
      if domain != 'CONUS':
        wedgj_utils.plot_counties(self, ax)
      
      #Add cartopy boundaries:
      wedgj_utils.add_geog_ref(self, ax)

    plt.tight_layout()

    if spath != None:
      plt.savefig('{}/{}_{}_D4_8.png'.format(spath, date.strftime("%Y%m%d"), domain), dpi = 300)
    else:
      pass
