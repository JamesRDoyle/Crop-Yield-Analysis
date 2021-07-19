# James Doyle
# Code to read in cleaned weather/yield data and process it for analysis


# Editable variables
base_filepath = '~/Processed_Data/'

# Importing necessary packages
import pandas as pd 


# Import data into pandas DataFrames
corn_yield = pd.read_csv(base_filepath+'Cleaned_Corn_Yield.csv')
soybean_yield = pd.read_csv(base_filepath+'Cleaned_Soybean_Yield.csv')
wheat_yield = pd.read_csv(base_filepath+'Cleaned_Wheat_Yield.csv')
areas_of_interest = pd.read_csv(base_filepath+'Areas_of_Interest.csv')

# Turn the ANSI codes for yield DataFrames into the proper string format
corn_yield['ANSI Code'] = corn_yield['ANSI Code'].astype(str).str.zfill(5)
soybean_yield['ANSI Code'] = soybean_yield['ANSI Code'].astype(str).str.zfill(5)
wheat_yield['ANSI Code'] = wheat_yield['ANSI Code'].astype(str).str.zfill(5)

# Find the counties of interest for each specific crop
corn_counties = [str(i).zfill(5) for i in corn_yield['ANSI Code'].unique().tolist()]
soybean_counties = [str(i).zfill(5) for i in soybean_yield['ANSI Code'].unique().tolist()]
wheat_counties = [str(i).zfill(5) for i in wheat_yield['ANSI Code'].unique().tolist()]

# Turn all ANSI codes in areas_of_interest into the proper string format
areas_of_interest['ANSI Code'] = areas_of_interest['ANSI Code'].astype(str).str.zfill(5)
# Turns the ANSI codes into the indices of areas_of_interest
areas_of_interest.set_index('ANSI Code', inplace=True)


# ---------------------------
# 	   Main program code:
# ---------------------------
def main():
	# Use the create_drought_data() method to process and create data for each crop
	crop_list = ['Corn', 'Soybean', 'Wheat']
	for crop in crop_list:
		crop_complete = create_drought_data(crop)
		crop_complete.to_csv(r''+base_filepath+'Final_Data/'+crop+'_Droughts.csv', index=False, header=True)



#--------------------------------------------------------------------------------
# Method definition to create and return the DataFrame with drought information.
#--------------------------------------------------------------------------------
def create_drought_data(crop_type):
	# Sets up loop and data file requirements depending on the type of crop
	if (crop_type == 'Corn'):
		yield_df = corn_yield
		counties = corn_counties
		#counties = ['17079', '18095']  # TEMPORARY ASSIGNMENT, REMOVE LATER!!!
		years = range(1991, 2020+1)
		dates = ['-04-01', '-10-31']
	elif (crop_type == 'Soybean'):
		yield_df = soybean_yield
		counties = soybean_counties
		#counties = ['28115', '38021']  # TEMPORARY ASSIGNMENT, REMOVE LATER!!!
		years = range(1991, 2020+1)
		dates = ['-05-01', '-11-30']
	elif (crop_type == 'Wheat'):
		yield_df = wheat_yield
		counties = wheat_counties
		#counties = ['06095', '51057']  # TEMPORARY ASSIGNMENT, REMOVE LATER!!!
		years = range(1991, 2020+1)
		dates = ['-11-01', '-07-31']
		return create_wheat_drought_data(yield_df=yield_df, counties=counties, years=list(years), dates=dates)
	else:
		raise Exception("Improper crop type submitted. Please pass 'corn', 'soybean', or 'wheat'.")

	# Create new dataframes to store drought information for each crop using custom drought durations
	droughts = pd.DataFrame(columns=['Year', 'County', 'State', 'Location', #'Yield Value',
									 'Num_Short', 'Periods_S', 'Lengths_S',
									 'Num_Med', 'Periods_M', 'Lengths_M',
									 'Num_Long', 'Periods_L', 'Lengths_L',
									 'Total Short Time', 'Total Med Time', 'Total Long Time',
									 'Total Drought Time', 'Total Drought Percentage'])

	# Create a new row in the DataFrame for each county/year combination
	print(f'\nDrought calculations for {crop_type}:')
	for county in counties:
		print("Calculating drought data for "+areas_of_interest.loc[county, 'Location'])
		state = areas_of_interest.loc[county, 'State Initial']

		# Reads in the weather data set and sets the date column as the index
		weather = pd.read_csv(base_filepath+'Weather_Data/'+state+'_AVGPrecip.csv')
		weather['Date'] = pd.to_datetime(weather['Date'])
		weather.set_index('Date', inplace=True)

		# For each year of interest
		for year in years:
			# Establish the growing season that crosses years
			growth_season = pd.date_range(start=str(year)+dates[0], end=str(year)+dates[1])

			# Calculate the drought data for this county in this year and append it to the DataFrame
			data = calculate_droughts(yield_df=yield_df, county=county, state=state, year=year, 
									  growth_season=growth_season, weather_df=weather)
			droughts = droughts.append(data, ignore_index=True)

		# End of drought data for a single county, loop is repeated for more counties

	yield_df = yield_df[['Year', 'ANSI Code', 'Value']].rename(columns={'ANSI Code':'County', 'Value':'Yield Value'})
	return droughts.merge(right=yield_df, how='left', on=['Year', 'County'])


#---------------------------------------------------------------------------
# Modified version of the original create_drought_data() method to support 
# planting/harvesting in separate calendar years.
#---------------------------------------------------------------------------
def create_wheat_drought_data(yield_df, counties, years, dates, crop_type='wheat'):
	# Create new dataframes to store drought information for each crop using custom drought durations
	droughts = pd.DataFrame(columns=['Year', 'County', 'State', 'Location',
									 'Num_Short', 'Periods_S', 'Lengths_S',
									 'Num_Med', 'Periods_M', 'Lengths_M',
									 'Num_Long', 'Periods_L', 'Lengths_L',
									 'Total Short Time', 'Total Med Time', 'Total Long Time',
									 'Total Drought Time', 'Total Drought Percentage'])
	start_year = years.pop(0)

	print(f'\nDrought calculations for {crop_type}:')
	for county in counties:
		print("Calculating drought data for "+areas_of_interest.loc[county, 'Location'])
		state = areas_of_interest.loc[county, 'State Initial']

		# Reads in the weather data set and sets the date column as the index
		weather = pd.read_csv(base_filepath+'Weather_Data/'+state+'_AVGPrecip.csv')
		weather['Date'] = pd.to_datetime(weather['Date'])
		weather.set_index('Date', inplace=True)

		# For each year of interest
		for year in years:
			# Establish the growing season that crosses years
			growth_season = pd.date_range(start=str(year-1)+dates[0], end=str(year)+dates[1])

			# Calculate the drought data for this county in this year and append it to the DataFrame
			data = calculate_droughts(yield_df=yield_df, county=county, state=state, year=year, 
									  growth_season=growth_season, weather_df=weather)
			droughts = droughts.append(data, ignore_index=True)

		# End of drought data for a single county, loop is repeated for more counties

	yield_df = yield_df[['Year', 'ANSI Code', 'Value']].rename(columns={'ANSI Code':'County', 'Value':'Yield Value'})
	return droughts.merge(right=yield_df, how='left', on=['Year', 'County'])


#---------------------------------------------------------------------------
# Method to calculate the drought data for each growing season then returns 
# the data as a dictionary. This method is called by the others to do the 
# actual calculations.
#---------------------------------------------------------------------------
def calculate_droughts(yield_df, county, state, year, growth_season, weather_df):
	# Count the number of short, medium, and long length droughts
	cur_len = 0
	s_date, e_date = '', ''
	total_s, total_m, total_l = 0, 0, 0
	num_days = 0

	# Create variable counters to later store in the data dictionary
	num_short, periods_s, lengths_s = 0, '', ''
	num_med, periods_m, lengths_m = 0, '', ''
	num_long, periods_l, lengths_l = 0, '', ''
	
	for day in growth_season:
		num_days += 1
		if (weather_df.loc[day, county] <= 0.00005):  # None to negligible rain -> increase drought length counter
			if cur_len == 0:
				s_date = day  # Start a new drought if necessary
			cur_len += 1

		# Rain has occured and a drought has ended, so end the drought & record drought data to the DataFrame
		elif (weather_df.loc[day, county] > 0.00005 and cur_len >= 5):
			e_date = day  # End date is the first day of rain after drought

			if (cur_len in range(5,9)):  # Short Drought
				num_short += 1
				total_s += cur_len
				if (periods_s!='' and lengths_s!=''):
					periods_s += ', '+str(s_date.date())+' to '+str(e_date.date())
					lengths_s += ', '+str(cur_len)
				else:
					periods_s = str(s_date.date())+' to '+str(e_date.date())
					lengths_s = str(cur_len)

			elif (cur_len in range(9,15)):  # Medium Drought
				num_med += 1
				total_m += cur_len
				if (periods_s!='' and lengths_s!=''):
					periods_s += ', '+str(s_date.date())+' to '+str(e_date.date())
					lengths_s += ', '+str(cur_len)
				else:
					periods_m = str(s_date.date())+' to '+str(e_date.date())
					lengths_m = str(cur_len)

			elif (cur_len >= 15):  # Long Drought
				num_long += 1
				total_l += cur_len
				if (periods_l!='' and lengths_l!=''):
					periods_l += ', '+str(s_date.date())+' to '+str(e_date.date())
					lengths_l += ', '+str(cur_len)
				else:
					periods_l = str(s_date.date())+' to '+str(e_date.date())
					lengths_l = str(cur_len)

			cur_len = 0  # Reset drought duration now that it has ended
			s_date, e_date = '', ''  # Reset drought dates

		else:  # Area got precipitation but no drought was ended: reset the counter
			cur_len = 0 
			s_date, e_date = '', ''  # Reset drought dates

	# Update the data dictionary with the correct information then return it
	total_drought = total_s+total_m+total_l
	data = {'Year':year, 'County':county, 'State':state, 
			'Location':areas_of_interest.loc[county, 'Location'],
			'Num_Short':num_short, 'Periods_S':periods_s, 'Lengths_S':lengths_s,
			'Num_Med':num_med, 'Periods_M':periods_m, 'Lengths_M':lengths_m,
			'Num_Long':num_long, 'Periods_L':periods_l, 'Lengths_L':lengths_l,
			'Total Short Time':total_s, 'Total Med Time':total_m, 'Total Long Time':total_l,
			'Total Drought Time':total_drought, 
			'Total Drought Percentage':total_drought/num_days
			}
	return data



# ----------------------------------------------
# Run the main method to run the important code
# ----------------------------------------------
main()

print('Data has been processed and drought data has been calculated.')
