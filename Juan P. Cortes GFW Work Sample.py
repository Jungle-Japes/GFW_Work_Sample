#!/usr/bin/env python
# coding: utf-8

# # Work Sample Exercise – Junior Data Specialist – Global Forest Watch.
# 
# In this work sample, we will answer and do the following questions:
# 
# 1) How large/ how many rows are in the dataset?
# 2) What is the spatial extent of the dataset?
# 3) How many mills have an unknown parent company?
# 4) Which country has the most palm oil mills?
# 5) Map the palm oil mills, distinguishing those that are RSPO Certified from those that are not.
# 
# This will be done primarily through python and its associated packages. The notebook will also demonstrate how to use the google maps api to create alternative maps. Here we go!

# ### First we must import packages and read in the data to prepare the analysis.

# In[1]:


# Import all of the packages that are necessary for the demonstration.
# Pandas will be used for reading in uml.csv as well as analyzing it
# Geopandas is used to facilitate working with spatial data
# shapely.geometry is a package that works with Geopandas and creates geometric objects
# matplotlib will allow the script to map out objects

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

#the magic function runs on the backend and allows plots to be shown beneath each kernel 

get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


# read in csv and save it to variable df using pandas

df = pd.read_csv('uml.csv')


# In[3]:


# By using a lambda function, the points variable contains a loop in which the Longitude and Latitude
# columns are looped over and turned into Point objects. This allows data manipulation with geopandas

points = df.apply(lambda row: Point(row.Longitude, row.Latitude), axis=1)
points.head(3)


# In[4]:


# GeoDataFrames are like normal data frames but with geometry attached to them.
# The mills variable creates a new column which is equal to the previously made variable points (right-most column).

mills = gpd.GeoDataFrame(df, geometry = points)

# Ensures that the dataframe views geometry as latitude and longitude values

mills.crs = {'init': 'epsg:4326'}
mills.head(3)


# # 1) How large/ how many rows are in the dataset?

# In[5]:


# Shows how many rows, or the length of the dataframe.

len(df)


# ## The dataset is 1818 rows long. 

# # 2) What is the spatial extent of the dataset?

# ### There are two ways to do this, by finding out the 'corners', or the uppermost and bottommost points of the Longitude and Latitude columns of our data, or by visually projecting it.

# In[6]:


# Creates two variables. Both are lists which take the max and min of the longitude and latitude columns.

upper = [df.Longitude.max(), df.Latitude.max()]
lower = [df.Longitude.min(), df.Latitude.min()]

print (upper)
print (lower)


# ### The coordinates above represent the 'bounding box' of our dataset, but they aren't easily understandable. The next step will plot the entire dataset onto a map.

# In[7]:


# Brings in basic world map from the Geopandas library.

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Creates basic configuration for the map. This includes size, color, boundary color, and background color.

ax = world.plot(figsize = (24, 50), color='lightgreen', edgecolor='black')
ax.set_facecolor('aqua')

# Takes the mills variable, which read in all of the lat long values in the df and plots them onto the map.

mills.plot(ax=ax, color='red', zorder=1)

# Creates a title for map and indicates fontsize

plt.title('Palm Oil Mills', color='black', fontsize = 50)
plt.show()


# ### The same data can also be displayed using the google maps api, which make the map interactive rather than a static image.

# In[8]:


# Import the necessary packages. gmaps allows the api key to be registered, as well as use the functions within it.

import gmaps

# Using pandas, the line creates a subset the uml.csv table. It takes only the latitude and longitude coordinates,
# which will then be plotted onto the map.

locations = df[['Latitude', 'Longitude']]

# Creates the basemap, instructs what type of map it will be (heatmap) and adds the locations variable to the map.

fig = gmaps.figure()
symbol = gmaps.heatmap_layer(locations)
fig.add_layer(symbol)
fig


# ## The map demonstrates the extent of the dataset. It stays within mid-latitudes and spans throughout many countries, from Mexico to the Solomon Islands.

# # 3) How many mills have an unknown parent company?

# ### By querying the dataset with pandas the script will find out. First it is important to find out if the Parent_Com column has any null(Nan) values.

# In[9]:


# Finds out if there are any null values within the Parent_Com column.

df.Parent_Com.isnull().sum()


# ### Since there are none, find if Unknown or unknown are spelt differently

# In[10]:


# Sorts through the Parent_Com column for any values that are equal to either spelling of unknown.

df[(df.Parent_Com == 'Unknown') | (df.Parent_Com == 'unknown')]


# ## By sorting through both spellings, and looking at the amount of rows, there are 93 mills with an unknown parent company.

# # 4) Which country has the most palm oil mills?

# In[11]:


# Points out the most recurring value in the 'Country' column.

df['Country'].value_counts().idxmax()


# ### Indonesia has the most, but the command didn't specify how many. The next line will. 

# In[12]:


# Points out a list of the most recurring values in the column in order from greatest to least.

df['Country'].value_counts()


# ## The country with the most mills is Indonesia with 1043 mills.

# # 5) Map the palm oil mills, distinguishing those that are RSPO Certified from those that are not.

# ### The first step is to separate those mills that are certified from those that are not.

# In[13]:


# Certified and non_certified take all rows in which the column value equals the expressions 'RSPO Certified'
# or 'Not RSPO Certified'. Using the .loc function from pandas, itt creates a subset of data and
# assigns it to their respective variables.

certified = mills.loc[df['RSPO_STATU'] == 'RSPO Certified']
not_certified = mills.loc[df['RSPO_STATU'] == 'Not RSPO Certified']

print (certified.count())
print (not_certified.count())


# ### By printing out the result of both variables, there are  356 certified mills, and 1462 non certified mills.

# ### Next is to create a map and plot the variables onto it.

# In[14]:


# Creates basic configuration for the map. This includes size, color, boundary color, and background color.

ax = world.plot(figsize = (40, 40), color='lightgreen', edgecolor='black')
ax.set_facecolor('aqua')

# Takes the certified and not_certified variables and plots them onto the map.

certified.plot(ax=ax, color='red', alpha=1, zorder=2)
not_certified.plot(ax=ax, color='blue', alpha=1, zorder=1)

# Creates a title for map and indicates fontsize

plt.title('Certified(Blue) and Not Certified(Red) Palm Oil Mills', color='black', fontsize = 60)
plt.show()


# ### Once again, the data can be displayed using the Google maps api key to make the map interactive.

# In[15]:


# Certified and non_certified take all rows in which the column value equals the expressions 'RSPO Certified'
# or 'Not RSPO Certified'. Using the .loc function from pandas, itt creates a subset of data and
# assigns it to their respective variables.

certified = mills.loc[df['RSPO_STATU'] == 'RSPO Certified']
not_certified = mills.loc[df['RSPO_STATU'] == 'Not RSPO Certified']

# The map needs to read in the Latitude and Longitude values to plot out the data. Since the certified and
# not_certified are subsets of the original csv, the lines below will create variables which read the 
# Latitude and Longitude columns of each variable. Basically, a filter of a filter.
 
certified_subset = certified[['Latitude', 'Longitude']]
not_certified_subset = not_certified[['Latitude', 'Longitude']]

# The variables below take the certified_subset and not_certified_subset, create symbol layers, and assign colors
# to them. Blue for certified mills, red for not certified mills.

symbol_1 = gmaps.symbol_layer(certified_subset, fill_color='blue', stroke_color='blue', scale=2)
symbol_2 = gmaps.symbol_layer(not_certified_subset, fill_color='red', stroke_color='red', scale=2)

# Creates the basemap, instructs what type of map it will be (heatmap) and adds the locations variable to the map.

fig = gmaps.figure()
fig.add_layer(symbol_2)
fig.add_layer(symbol_1)
fig


# # Description of blog on blog.globalforestwatch.org
# 
# https://blog.globalforestwatch.org/commodities/getting-at-the-source-universal-mill-list-improves-traceability-of-palm-oil-supply-chains?utm_campaign=gfw&amp;utm_source=gfwblog&amp;utm_medium=hyperlink&amp;utm_term=umlv2_11_2019

# ### Palm oil mills have complex supply chains, which makes it difficult to monitor their practices and impact on deforestation. The Universal Mill List (UML) is an open-source data file which centralizes and standardizes information about palm oil mills throughout the world. It is especially useful because it facilitates verification, sharing, and ensures that no mills are double counted through its universal ID system. The UML improves industry transparency, and helps companies ensure their commitment to sustainable development.
