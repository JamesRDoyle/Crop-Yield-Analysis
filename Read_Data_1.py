# James Doyle
# Code to read crop yield CSV files then process them into more usable forms


# Editable variables
base_filepath = '~/'

# Import needed packages
import pandas as pd


# Import data into pandas DataFrames
yield_data_path = base_filepath + 'Raw_Data/Yield_Data/'

corn_yield_1 = pd.read_csv(yield_data_path + "Corn Yield - Alabama to Oklahoma.csv")
corn_yield_2 = pd.read_csv(yield_data_path + "Corn Yield - Oregon to Wyoming.csv")
corn_yield = pd.concat([corn_yield_1, corn_yield_2])
del corn_yield_1
del corn_yield_2

soybean_yield = pd.read_csv(yield_data_path + "Soybean Yield - All Regions.csv")

wheat_yield = pd.read_csv(yield_data_path + "Wheat Yield - All Regions.csv")



# Clean data by removing unnecessary columns from corn, soybean, & wheat yield data
unneeded_yield_columns = ['Program', 'Period', 'Week Ending', 'Geo Level', 
				 		  'Zip Code', 'Region', 'watershed_code', 'Watershed', 
				 		  'Commodity', 'Data Item', 'Domain', 'Domain Category', 
				 		  'Ag District Code', 'CV (%)']
corn_yield = corn_yield.drop(unneeded_yield_columns, axis=1)
soybean_yield = soybean_yield.drop(unneeded_yield_columns, axis=1)
wheat_yield = wheat_yield.drop(unneeded_yield_columns, axis=1)
del unneeded_yield_columns


# Sorts yield data columns by Year, then State, then County
corn_yield = corn_yield.sort_values(by=['Year', 'State', 'County'], ascending=[False, True, True])
soybean_yield = soybean_yield.sort_values(by=['Year', 'State', 'County'], ascending=[False, True, True])
wheat_yield = wheat_yield.sort_values(by=['Year', 'State', 'County'], ascending=[False, True, True])


# Removes row values with a county of Other (prevents misc data from affecting values)
corn_yield = corn_yield[corn_yield['County'] != 'OTHER COUNTIES']
soybean_yield = soybean_yield[soybean_yield['County'] != 'OTHER COUNTIES']
wheat_yield = wheat_yield[wheat_yield['County'] != 'OTHER COUNTIES']
corn_yield = corn_yield[corn_yield['County'] != 'OTHER (COMBINED) COUNTIES']
soybean_yield = soybean_yield[soybean_yield['County'] != 'OTHER (COMBINED) COUNTIES']
wheat_yield = wheat_yield[wheat_yield['County'] != 'OTHER (COMBINED) COUNTIES']


# Converts State, County, and Ag District names to title case (aka proper case)
cols = ['State', 'County', 'Ag District']
for col in cols:
	corn_yield[col] = corn_yield[col].str.title()
	soybean_yield[col] = soybean_yield[col].str.title()
	wheat_yield[col] = wheat_yield[col].str.title()
del cols


# Creates a new column to store the State-County combination
# This allows for the differentiation of same-named counties in different states (ex. Washington County)
corn_yield['Location'] = corn_yield['County'] + ' County, ' + corn_yield['State']
soybean_yield['Location'] = soybean_yield['County'] + ' County, ' + soybean_yield['State']
wheat_yield['Location'] = wheat_yield['County'] + ' County, ' + wheat_yield['State']


# Creates a new column to store the complete ANSI (FIPS) code (used in retrieving weather data)
corn_yield['ANSI Code'] = corn_yield['State ANSI'].astype(str).str.zfill(2) + corn_yield['County ANSI'].astype(int).astype(str).str.zfill(3)
soybean_yield['ANSI Code'] = soybean_yield['State ANSI'].astype(str).str.zfill(2) + soybean_yield['County ANSI'].astype(int).astype(str).str.zfill(3)
wheat_yield['ANSI Code'] = wheat_yield['State ANSI'].astype(str).str.zfill(2) + wheat_yield['County ANSI'].astype(int).astype(str).str.zfill(3)
# Now removes partial ANSI code columns from DataFrames
corn_yield = corn_yield.drop(['State ANSI', 'County ANSI'], axis=1)
soybean_yield = soybean_yield.drop(['State ANSI', 'County ANSI'], axis=1)
wheat_yield = wheat_yield.drop(['State ANSI', 'County ANSI'], axis=1)


# Subset yield data by counties with at 30 years of data (in other words, data must be complete)
corn_yield = corn_yield[corn_yield.groupby('Location')['Location'].transform('count').ge(30)]
soybean_yield = soybean_yield[soybean_yield.groupby('Location')['Location'].transform('count').ge(30)]
wheat_yield = wheat_yield[wheat_yield.groupby('Location')['Location'].transform('count').ge(30)]


# Create a new DataFrame to store the States, Counties, Locations, and ANSI codes of interest
corn_subset = corn_yield[['State', 'County', 'Location', 'ANSI Code']].drop_duplicates()
soybean_subset = soybean_yield[['State', 'County', 'Location', 'ANSI Code']].drop_duplicates()
wheat_subset = wheat_yield[['State', 'County', 'Location', 'ANSI Code']].drop_duplicates()
areas_of_interest = pd.concat([corn_subset, soybean_subset, wheat_subset]).drop_duplicates().sort_values(by=['State', 'County'])


# Add a new column to areas_of_interest to store the state initial (ex. 'IN' for Indiana)
state_df = pd.read_csv(base_filepath + 'Raw_Data/State.csv', sep='|').drop(['STATE', 'STATENS'], axis=1)
state_df.columns = ['State Initial', 'State']
areas_of_interest = areas_of_interest.merge(state_df, how='inner', on='State')


# Add state initial columns to Corn_Yield, Soybean_Yield, and Wheat_Yield DataFrames
corn_yield = corn_yield.merge(state_df, how='inner', on='State')
soybean_yield = soybean_yield.merge(state_df, how='inner', on='State')
wheat_yield = wheat_yield.merge(state_df, how='inner', on='State')


# Export processed DataFrames into new CSV files
corn_yield.to_csv(r''+base_filepath+'Processed_Data/Cleaned_Corn_Yield.csv', index=False, header=True)
soybean_yield.to_csv(r''+base_filepath+'Processed_Data/Cleaned_Soybean_Yield.csv', index=False, header=True)
wheat_yield.to_csv(r''+base_filepath+'Processed_Data/Cleaned_Wheat_Yield.csv', index=False, header=True)
areas_of_interest.to_csv(r''+base_filepath+'Processed_Data/Areas_of_Interest.csv', index=False, header=True)



print("\nData reading & processing is now fully completed!\n")

