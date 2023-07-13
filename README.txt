The Wedgj package contains the spc_outlook, storm, noaa_performance, and winter modules.

Wedgj is a comprehensive package that allows users to explore different types of publicly available severe weather-related data. None of the functions within wedgj require any input to successfully run, but an empty call will return the most recent data displayed at the CONUS domain extent. For archived data in any of the functions, use the form: date = datetime(YYYY, M, D, H, M). Future plans include adding LSRs, TOR/SVR WWs, and radar archives. 

Any questions or suggestions should be directed to Andrew Blackford at acb0068@uah.edu .

Written by Andrew Blackford
Atmospheric and Earth Science Department
University of Alabama in Huntsville, June 2023

Required modules for complete functionality are:
- Python 3+
- geopandas (>=0.13.0, except 0.13.1)
- cartopy (>=0.21.0)
- pygrib
- Numpy
- Matplotlib

Valid domain inputs for mapping that are supported at this time for wedgj are:
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

------------------------------------INSTALLATION------------------------------------

The Wedgj package may be installed with pip:

    pip install git+https://github.com/acblackford/wedgj


Or manually:

  Get PySonde:
    git clone https://github.com/acblackford/wedgj
    cd wedgj
    python3 setup.py install
    cd ..

----------------------------------CURRENT FEATURES----------------------------------

** The spc_plot class currently only supports dates from October 16, 2019 to Present. Future plans are to extend capabilities to the entire database. **

The function spc_plot.day1_2_outlook can take the following inputs: 
date (a datetime object)
spath (string, path to save the figure if desired)
domain (string, from the above list)
outlook_day (string, 'day1' or 'day2')

The function spc_plot.day3_outlook can take the following inputs: 
date (a datetime object- the hour and minute fields are not required)
spath (string, path to save the figure if desired)
domain (string, from the above list)

The function spc_plot.day4_8_outlook can take the following inputs: 
date (a datetime object- the hour and minute fields are not required)
spath (string, path to save the figure if desired)
domain (string, from the above list)

** The storm class currently only supports dates from June 1, 1999 to Present when calling the storm_reports function, January 1, 2002 to Present when calling the sbw function, and January 1, 1950 to December 31st, 2022 when calling the tor_plot function. **

The function storm.storm_reports can take the following inputs: 
date (a datetime object)
spath (string, path to save the figure if desired)
domain (string, from the above list)
report_type (string, options are: 'All', 'Tornado', 'Wind', and 'Hail')
The function storm.storm_reports can also read user-formatted georeferenced data and countour it underneath the storm report locations on a map. The following arguments are set to None, but if data is input, all three arguments must be passed by the user.
data (Requires data to be in a dictionary with data['lats'], data['lons'], and data['values'])
data_cint (range of values to contour user-input data, example format is cint = np.arange(10., 101., 10.)
data_levels (range of values to contour-fill user-input data, example format is cfint = np.arange(0.1, 51.,2.5))

The function storm.sbw can take the following inputs:
start_date (a datetime object)
end_date (a datetime object)
spath (string, path to save the figure if desired)
domain (string, from the above list)
warn_type (string, options are: 'All', 'TOR', 'SVR', and 'FFW')

The function tor_plot can take the following inputs:
start_date (a datetime object)
end_date (a datetime object)
spath (string, path to save the figure if desired)
domain (string, from the above list)
tor_type (string, options are: 'Both', 'Points', and 'Paths') 
rating (string, options are 'All', 'Significant', 'Violent', 'FAT', 'INJ', 'UNK', '0', '1', '2', '3', '4', and '5')

Note: tor_type('Points') will plot touchdown locations of the tornadoes.

** The noaa_performance class currently only supports dates from October 16, 2019 to Present. Future plans are to extend capabilities to the entire database. **

The fuction noaa_performance can take the following inputs:
date (a datetime object)
spath (string, path to save the figure if desired)
domain (string, from the above list)
report_type (string, options are: 'All', 'Tornado', 'Wind', and 'Hail')
warn_type (string, options are: 'All', 'TOR', 'SVR', and 'FFW')
The function noaa_performance can also read user-formatted georeferenced data and countour it underneath the storm report locations on a map. The following arguments are set to None, but if data is input, all three arguments must be passed by the user.
data (Requires data to be in a dictionary with data['lats'], data['lons'], and data['values'])
data_cint (range of values to contour user-input data, example format is cint = np.arange(10., 101., 10.)
data_levels (range of values to contour-fill user-input data, example format is cfint = np.arange(0.1, 51.,2.5))

** The winter class currently only supports the most recent model files, using utcnow to find the time. Future plans are to extend capabilities to the archived files. **

The function hrrr_ice can take the following inputs:
spath (string, path to save the figure if desired)
domain (string, from the above list)

The function hrrr_snow can take the following inputs:
spath (string, path to save the figure if desired)
domain (string, from the above list)
type (string, options are: '10:1', 'model', and 'kuchera')

------------------------------------------EXAMPLES------------------------------------------

***See Examples folder for a Google Colab and Jupyter notebook of examples using wedgj***   
    
