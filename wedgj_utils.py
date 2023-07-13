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
import matplotlib.colors as mcolors

######------ extent_table ------######
# extent_table returns a list of     # 
# pre-determined extent coordinates  #
# for each valid domain input        #
######################################

def extent_table(self):
    extent_table = {'Midwest': (-99.2, -78.27, 36.48, 49.64), 'Northeast': (-84.93, -66.21, 35.99, 47.68), 
                    'Southeast': (-95.39, -75.17, 24.50, 37.35), 'TN Valley': (-92, -81, 33, 39.3), 'Southern Plains': (-109.55, -90.34, 24.94, 40.38), 
                    'Northern Plains': (-106.71, -94.14, 39.15, 49.48), 'Northwest': (-125.37, -103.47, 40.75, 49.48),
                    'Southwest': (-125.21, -101.77, 30.97, 42.22), 'Ohio': (-85.14, -80.17, 37.92, 42.19),
                    'Indiana': (-88.97, -83.84, 37.32, 41.92), 'Alabama': (-89.65, -83.87, 29.64, 35.36),
                    'CONUS': (-127.0, -65.5, 23.0, 49.0)}
                    
    return extent_table

######------ figsize_table ------######
# figsize_table returns a list of     # 
# pre-determined best-fit figsizes    #
# for each valid domain input         #
#######################################

def figsize_table(self):
    figsize_table = {'Midwest': (8.5, 13), 'Northeast': (9, 12), 
              'Southeast': (10,13), 'TN Valley': (9,12), 'Southern Plains': (8,16), 
              'Northern Plains': (7,11), 'Northwest': (11,9),
              'Southwest': (11.5,11), 'Ohio': (7.5,12),
              'Indiana': (7.5,12.5), 'Alabama': (9,12),
              'CONUS': (15,13)}
    
    return figsize_table

######------ add_geog_ref ------######
# add_geog_ref adds and formats all  # 
# desired cartopy boundaries to the  #
# domain of choice                   #
######################################

def add_geog_ref(self, ax):
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

#####------ plot_counties ------#####
# plot_counties will load in an in- # 
# house county shapefile to plot on #
# regional and state domains        #
#####################################
    
def plot_counties(self, ax):
    reader = shpreader.Reader('wedgj/Shapefiles/US_Counties/US_Counties.shp')

    county = list(reader.geometries())
    county_lines = cfeature.ShapelyFeature(county, ccrs.crs.PlateCarree())


    ax.add_feature(county_lines, lw = 0.1, edgecolor = 'black', facecolor = 'None')
    
    
######------ plot_oh_cities ------######
# plot_oh_cities adds desired Ohio     # 
# major cities to the state scene      #
# with their names labeled             #
########################################

def plot_oh_cities(self, ax):
    Dayton = gpd.tools.geocode('Dayton, OH')
    Cincinnati = gpd.tools.geocode('Cincinnati, OH')
    Columbus = gpd.tools.geocode('Columbus, OH')
    Cleveland = gpd.tools.geocode('Cleveland, OH')
    Toledo = gpd.tools.geocode('Toledo, OH')
    Akron = gpd.tools.geocode('Akron, OH')
    Lima = gpd.tools.geocode('Lima, OH')

    oh_cities = [Dayton['geometry'][0], Cincinnati['geometry'][0], Columbus['geometry'][0], Cleveland['geometry'][0], Toledo['geometry'][0], Akron['geometry'][0], Lima['geometry'][0]]
    oh_x = [point.x for point in oh_cities]
    oh_y = [point.y for point in oh_cities]

    oh_cities_labels = [Dayton['address'][0].split(',')[0], Cincinnati['address'][0].split(',')[0], Columbus['address'][0].split(',')[0], Cleveland['address'][0].split(',')[0], Toledo['address'][0].split(',')[0], Akron['address'][0].split(',')[0], Lima['address'][0].split(',')[0]]
    ax.scatter(oh_x, oh_y, color = 'None', edgecolor = 'black', s = 100, marker = 's', linewidths = 2, transform = ccrs.crs.PlateCarree(), zorder = 10)

    for i in range(len(oh_x)):
      ax.text(oh_x[i]+0.1, oh_y[i]+0.1, oh_cities_labels[i], horizontalalignment='left', verticalalignment='center', transform = ccrs.crs.PlateCarree(), fontweight = 'bold', font = 'Liberation Serif', fontsize = 14)

######------ plot_in_cities ------######
# plot_oh_cities adds desired Indiana  # 
# major cities to the state scene      #
# with their names labeled             #
########################################

def plot_in_cities(self, ax):
    Fort_Wayne = gpd.tools.geocode('Fort Wayne, IN')
    Indianapolis = gpd.tools.geocode('Indianapolis, IN')
    Muncie = gpd.tools.geocode('Muncie, IN')
    Gary = gpd.tools.geocode('Gary, IN')
    South_Bend = gpd.tools.geocode('South Bend, IN')
    Bloomington = gpd.tools.geocode('Bloomington, IN')
    Evansville = gpd.tools.geocode('Evansville, IN')
    Lafayette = gpd.tools.geocode('Lafayette, IN')

    in_cities = [Fort_Wayne['geometry'][0], Indianapolis['geometry'][0], Muncie['geometry'][0], Gary['geometry'][0], South_Bend['geometry'][0], Bloomington['geometry'][0], Evansville['geometry'][0], Lafayette['geometry'][0]]
    in_x = [point.x for point in in_cities]
    in_y = [point.y for point in in_cities]

    in_cities_labels = [Fort_Wayne['address'][0].split(',')[0], Indianapolis['address'][0].split(',')[0], Muncie['address'][0].split(',')[0], Gary['address'][0].split(',')[0], South_Bend['address'][0].split(',')[0], Bloomington['address'][0].split(',')[0],  Evansville['address'][0].split(',')[0],  Lafayette['address'][0].split(',')[0]]
    ax.scatter(in_x, in_y, color = 'None', edgecolor = 'black', s = 100, marker = 's', linewidths = 2, transform = ccrs.crs.PlateCarree(), zorder = 10)

    for i in range(len(in_x)):
      ax.text(in_x[i]+0.1, in_y[i]+0.1, in_cities_labels[i], horizontalalignment='left', verticalalignment='center', transform = ccrs.crs.PlateCarree(), fontweight = 'bold', font = 'Liberation Serif', fontsize = 14)


######------ plot_al_cities ------######
# plot_oh_cities adds desired Alabama  # 
# major cities to the state scene      #
# with their names labeled             #
########################################

def plot_al_cities(self, ax):
    Huntsville = gpd.tools.geocode('Huntsville, AL')
    Tuscaloosa = gpd.tools.geocode('Tuscaloosa, AL')
    Birmingham = gpd.tools.geocode('Birmingham, AL')
    Montgomery = gpd.tools.geocode('Montgomery, AL')
    Dothan = gpd.tools.geocode('Dothan, AL')
    Mobile = gpd.tools.geocode('Mobile, AL')

    al_cities = [Huntsville['geometry'][0], Tuscaloosa['geometry'][0], Birmingham['geometry'][0], Montgomery['geometry'][0], Dothan['geometry'][0], Mobile['geometry'][0]]
    al_x = [point.x for point in al_cities]
    al_y = [point.y for point in al_cities]

    al_cities_labels = [Huntsville['address'][0].split(',')[0], Tuscaloosa['address'][0].split(',')[0], Birmingham['address'][0].split(',')[0], Montgomery['address'][0].split(',')[0], Dothan['address'][0].split(',')[0],  Mobile['address'][0].split(',')[0]]
    ax.scatter(al_x, al_y, color = 'None', edgecolor = 'black', s = 100, marker = 's', linewidths = 2, transform = ccrs.crs.PlateCarree(), zorder = 10)

    for i in range(len(al_x)):
      ax.text(al_x[i]+0.1, al_y[i]+0.1, al_cities_labels[i], horizontalalignment='left', verticalalignment='center', transform = ccrs.crs.PlateCarree(), fontweight = 'bold', font = 'Liberation Serif', fontsize = 14)

######--------- snow_cmap --------######
# snow_cmap defines a custom colormap  # 
# for the winter class to utilize      #
# in mapping functions                 #
########################################

def snow_cmap(self):
    self.snow_clevs = [0, 1, 3, 5, 8, 12, 18 ,24, 36, 48, 54]

    snow_cmap_data = ['#56efff', # T-1
                    '#15AAD3', # 1-3
                    '#18849F', # 3-5
                    '#B3A2FE', # 5-8
                    '#975FFF', # 8-12
                    '#662FAD', # 12-18
                    '#FF50A6', # 18-24
                    '#FFB8FF', # 24-36
                    '#B9E2F8', # 36-48
                    '#D5FFFE', # 48+
                    
                    ]
    self.snow_cmap = mcolors.ListedColormap(snow_cmap_data, 'acc_snowfall')
    self.snow_norm = mcolors.BoundaryNorm(snow_clevs, snow_cmap.N)
    snow_table = {}
    return snow_table
    
######--------- ice_cmap ---------######
# ice_cmap defines a custom colormap   # 
# for the winter class to utilize      #
# in mapping functions                 #
########################################

def ice_cmap(self):
    ice_clevs = [0, 0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0]
    
    ice_cmap_data = ['#FEBCFE', # T-0.1"
                    '#FF67FF', # 0.1-0.25"
                    '#D639D6', # 0.25-0.5"
                    '#A219A2', # 0.5-0.75"
                    '#580658', # 0.75-1.0"
                    '#179AD4', # 1.0-1.5"
                    '#21D8EC', # 1.5"+
                    ]
    
    ice_table = {'ice_clevs': [0, 0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0], 'ice_cmap': mcolors.ListedColormap(ice_cmap_data, 'acc_ice')}
    return ice_table
