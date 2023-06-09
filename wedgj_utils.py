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

    oh_cities = [Dayton['geometry'][0], Cincinnati['geometry'][0], Columbus['geometry'][0], Cleveland['geometry'][0], Toledo['geometry'][0], Akron['geometry'][0]]
    oh_x = [point.x for point in oh_cities]
    oh_y = [point.y for point in oh_cities]

    oh_cities_labels = [Dayton['address'][0].split(',')[0], Cincinnati['address'][0].split(',')[0], Columbus['address'][0].split(',')[0], Cleveland['address'][0].split(',')[0], Toledo['address'][0].split(',')[0], Akron['address'][0].split(',')[0]]
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
    Decatur = gpd.tools.geocode('Decatur, AL')
    Tuscaloosa = gpd.tools.geocode('Tuscaloosa, AL')
    Birmingham = gpd.tools.geocode('Birmingham, AL')
    Montgomery = gpd.tools.geocode('Montgomery, AL')
    Dothan = gpd.tools.geocode('Dothan, AL')
    Mobile = gpd.tools.geocode('Mobile, AL')

    al_cities = [Huntsville['geometry'][0], Decatur['geometry'][0], Tuscaloosa['geometry'][0], Birmingham['geometry'][0], Montgomery['geometry'][0], Dothan['geometry'][0], Mobile['geometry'][0]]
    al_x = [poalt.x for point in al_cities]
    al_y = [poalt.y for point in al_cities]

    al_cities_labels = [Huntsville['address'][0].split(',')[0], Decatur['address'][0].split(',')[0], Tuscaloosa['address'][0].split(',')[0], Birmingham['address'][0].split(',')[0], Montgomery['address'][0].split(',')[0], Dothan['address'][0].split(',')[0],  Mobile['address'][0].split(',')[0]]
    ax.scatter(al_x, al_y, color = 'None', edgecolor = 'black', s = 100, marker = 's', lalewidths = 2, transform = ccrs.crs.PlateCarree(), zorder = 10)

    for i in range(len(al_x)):
      ax.text(al_x[i]+0.1, al_y[i]+0.1, al_cities_labels[i], horizontalalignment='left', verticalalignment='center', transform = ccrs.crs.PlateCarree(), fontweight = 'bold', font = 'Liberation Serif', fontsize = 14)


