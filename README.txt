# wedgj
Wedgj is a comprehensive package that allows users to explore different types of publicly available severe weather-related data.

Required packages for complete functionality are:
- geopandas (0.13.0 works best at this time)
- scipy
- metpy (future updates will not require metpy, as it is only used for a county shapefile at this time)
- pandas
- cartopy
- shapely

Valid domain inputs supported at this time for wedgj are:
- CONUS
- Midwest
- Northeast
- Southeast
- TN Valley
- Southern Plains
- Northern Plains
- Northwest
- Southwest
- Alabama
- Indiana
- Ohio

If no date is given, the most current data will populate. For archived data, use the form: date = datetime(YYYY, M, D, H, M)

** The spc_outlook class currently only supports dates from October 16, 2019 to Present. Future plans are to extend capabilities to the entire database. **

The function spc_outlook.day1_2_outlook can take the following inputs: 
date (a datetime object)
spath (string, path to save the figure if desired)
domain (string, from the above list)
outlook_day (string, 'day1' or 'day2')

The function spc_outlook.day3_outlook can take the following inputs: 
date (a datetime object- the hour and minute fields are not required)
spath (string, path to save the figure if desired)
domain (string, from the above list)

The function spc_outlook.day4_8_outlook can take the following inputs: 
date (a datetime object- the hour and minute fields are not required)
spath (string, path to save the figure if desired)
domain (string, from the above list)

** The storm class currently only supports dates from October 16, 2019 to Present. Future plans are to extend capabilities to the entire database. **

For the storm_reports function, valid report_type inputs are:

All
Tornado
Wind
Hail

For the sbw function, valid warn_type inputs are:

All
TOR
SVR
FFW

For the tor_plot function, valid tor_type inputs are:

Both
Points
Paths
and valid rating inputs are:

All
Significant
Violent
UNK
0
1
2
3
4
5
