# Background:
Through the use of Python data science tools, this toolset utilizes crop yield and weather data to enable the analysis of crop yield, weather, and drought data. Although much of what was done in this project could have been completed more easily using other tools (such as data file cleaning in Excel, graphing in R or Tableau, etc.), one of my personal goals for this project was to use as much Python as possible to simplify the amount of software knowledge needed to run these tools. This toolset was my project for the 2021 Purdue Data Science in Digital Agriculture REEU Program.

The extra packages required for this toolset are Pandas, Requests, Datetime, and Matplotlib. An internet connection is also required when using the API to retrieve weather data (Read_Data_2.py).

# How to Use:
I have included the original crop yield data files that I used (they were downloaded from USDA/NASS's QuickStats website at https://quickstats.nass.usda.gov) in the Raw_Data directory. I have also included in this directory a State.csv file that is used to merge State specific data such as initials to processed data (this data was retrieved from https://www.census.gov/library/reference/code-lists/ansi/ansi-codes-for-states.html). Read_Data_1.py will process and merge (if needed) crop yield data frames and remove all data that does not span the complete 30 years of interest (I downloaded the files containing data from 1991 up to 2020). The cleaned data is then exported to the Processed_Data directory to be later used.

The Read_Data_2.py program uses a custom API call to the Applied Climate Information System's database (I used the ACIS' QueryBuilder at http://builder.rcc-acis.org to set up the parameters for this call) to download the weather data for all years and regions of interest. The data is then exported into new files in the Processed_Data/Weather_Data directory (this file needs to be added manually). By default, Read_Data_2.py will download Average Temperature and Precipitation files, but the file can be modified to download Average Temperature, Precipitation, Maximum Temperature, and/or Minimum Temperature files depending on the desired analysis need. Note: The weather data has NOT been uploaded, so this program needs to be run before any more can be done (it can take a while to run, but print statements have been included in the code to allow for progress monitoring).

Process_Data.py merges crop yield and weather data into singular files before analysis. This program also calculates drought information such as the number of short, medium, and long length droughts (5-8, 9-14, & 15+ days respectively), the total precipitation, and the amount of time spent in drought. This program utilizes estimated growing seasons for each crop to limit the drought calculations to a certain time span, and these can be edited as needed (I have provided rough estimates based on the given data in the 1997 Usual Planting and Harvesting Dates for U.S. Field Crops available at https://usda.library.cornell.edu/concern/publications/vm40xr56k).

The Analyze_Data.py program brings together the data processed from the other tools into one analysis-focused program. The data is imported into this file and can be edited as desired by the user to do in depth analysis at the total, state, or county level. Some example graphs and data calculations are provided to guide your own analysis.
