The Wedgj package contains the spc_outlook and storm modules.

Wedgj is a comprehensive package that allows users to explore different types of publicly available severe weather-related data. None of the functions within wedgj require any input to successfully run, but an empty call will return the most recent data displayed at the CONUS domain extent. For archived data in any of the functions, use the form: date = datetime(YYYY, M, D, H, M). Future plans include adding LSRs, TOR/SVR WWs, and radar archives. 

Any questions or suggestions should be directed to Andrew Blackford at acb0068@uah.edu .

Written by Andrew Blackford
Atmopsheric and Earth Science Department
University of Alabama in Huntsville, June 2023

Required modules for complete functionality are:
- Python 3+
- geopandas (>=0.13.0, except 0.13.1)
- pandas
- cartopy
- Numpy
- Matplotlib
- metpy (future updates will not require metpy, as it is only used for a county shapefile at this time)

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
report_type(string, options are: 'All', 'Tornado', 'Wind', and 'Hail')
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

Note: storm.sbw currently only supports date ranges within the same calendar year. The next update to wedgj will include multi-year functionality.

The function tor_plot can take the following inputs:

For the tor_plot function, valid tor_type inputs are:
start_date (a datetime object)
end_date (a datetime object)
spath (string, path to save the figure if desired)
domain (string, from the above list)
tor_type (string, options are: 'Both', 'Points', and 'Paths') 
Note: 'Points' will plot touchdown locations of the tornadoes.
rating (string, options are 'All', 'Significant', 'Violent', 'UNK', '0', '1', '2', '3', '4', and '5')

Note: Contrary to storm.sbw, storm.tor_plot supports date ranges throughout multiple calendar years.

------------------------------------------EXAMPLES------------------------------------------

Example creation of the spc_plot.day1_2_outlook object to plot the Day 1 45% tornado risk day in the Southeast domain in March of 2021.

    from wedgj import spc_plot
    rdr = spc_plot.
    day1_2_outlook(date = datetime(2021,3,17,16,30), domain = 'Southeast', outlook_day = 'day1')

Example creation of the storm.sbw object to plot all tornado warnings in CONUS in the year 2019.
    from wedgj import storm
    rdr = storm.storm()
    rdr.sbw(start_date = datetime(2019,1,1,0,0), end_date = datetime(2019,12,31,23,59), warn_type = 'TOR')
    
    
