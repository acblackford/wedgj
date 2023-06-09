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
      ax.text(oh_x[i]+0.1, oh_y[i]+0.1, oh_cities_labels[i], horizontalalignment='left', verticalalignment='center', transform = ccrs.crs.PlateCarree(), fontweight = 'bold', font = 'Liberation Serif', fontsize = 12)
