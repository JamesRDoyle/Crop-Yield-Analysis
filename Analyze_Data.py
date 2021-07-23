# James Doyle
# Code to read in processed data and analyze/plot it for my REEU Final Project


# Editable variables
base_filepath = '~/Processed_Data/'

# Importing necessary packages
import pandas as pd  
import matplotlib.pyplot as plt


# Import data sets as DataFrames from CSV files
areas_of_interest = pd.read_csv(base_filepath+'Areas_of_Interest.csv')
corn_data = pd.read_csv(base_filepath+'Final_Data/Corn_Droughts.csv')
soybean_data = pd.read_csv(base_filepath+'Final_Data/Soybean_Droughts.csv')
wheat_data = pd.read_csv(base_filepath+'Final_Data/Wheat_Droughts.csv')


# List containing all of the crop files read in and the crop name
crop_DFs = [[corn_data, 'Corn'], [soybean_data, 'Soybean'], [wheat_data, 'Wheat']]  


# Set up plot settings
plt.style.use('seaborn')
plt.rc('font', size=20)          # controls default text sizes
plt.rc('axes', titlesize=20)     # fontsize of the axes title
plt.rc('axes', labelsize=20)     # fontsize of the x and y labels
plt.rc('xtick', labelsize=20)    # fontsize of the tick labels
plt.rc('ytick', labelsize=20)    # fontsize of the tick labels
plt.rc('legend', fontsize=20)    # legend fontsize
plt.rc('figure', titlesize=20, figsize=(15, 8))  # fontsize of the figure title


#--------------------------------------------------------------------
# TEMPORARY REASSIGNMENT!!!!
#crop_DFs = [[wheat_data, 'Wheat']]
#--------------------------------------------------------------------
# Create descriptive statistics for each crop DataFrame
for df in crop_DFs:
	print('\nDescriptive statistics for all states for the number \nof short, medium, and long droughts ('+df[1]+' seasons):')
	columns = ['Num_Short', 'Num_Med', 'Num_Long']
	print(df[0][columns].describe().to_string())

	print('\nDescriptive statistics for all states for the time spent \nin short, medium, and long length droughts ('+df[1]+' seasons):')
	columns = ['Short_Time', 'Med_Time', 'Long_Time']
	print(df[0][columns].describe().to_string())

	print('\nDescriptive statistics for the state average of fraction of time spent in drought per '+df[1]+' season by state:')
	print(df[0].groupby('State')['Total Drought Percentage'].describe().to_string())
	


# Create and display a graph with the entire mean yield and entire mean time in drought
for df in crop_DFs:
	by_year = df[0].groupby(['Year'])
	ax = plt.subplot(3, 1, 1)
	plt.plot(by_year['Yield Value'].mean(), label='Average Yield', color='green')
	plt.legend(bbox_to_anchor=(1,1), loc="upper left")
	plt.ylabel('Yield (bu/A)')
	plt.title('Average Yield, Average Total Drought Time, & Mean Total Precipitation for '+df[1])

	plt.subplot(3, 1, 2, sharex=ax)
	plt.plot(by_year['Total Drought Time'].mean(), label='Mean Time in Drought', color='red')
	#plt.plot(by_year['Total Short Time'].mean(), label='Mean Time in Short Droughts')
	#plt.plot(by_year['Total Med Time'].mean(), label='Mean Time in Medium Droughts')
	#plt.plot(by_year['Total Long Time'].mean(), label='Mean in Long Droughts')
	plt.legend(bbox_to_anchor=(1,1), loc="upper left")
	plt.ylabel('Days in Drought')

	plt.subplot(3, 1, 3, sharex=ax)
	plt.plot(by_year['Total Precipitation'].mean(), label='Total Precipitation', color='blue')
	plt.legend(bbox_to_anchor=(1,1), loc="upper left")
	plt.ylabel('Precipitation (in.)')

	plt.tight_layout()
	plt.show()


# Create and display graphs for each state and each crop comparing average 
# crop yield and average total drought length
for df in crop_DFs:
	crop_DF = df[0].merge(areas_of_interest[['State', 'State Initial']], 
						  left_on='State', right_on='State Initial')
	for state in crop_DF['State_y'].unique():
		cur_state = crop_DF[crop_DF['State_y']==state]
		by_year = cur_state.groupby(['Year'])

		ax = plt.subplot(3, 1, 1)
		plt.plot(by_year['Yield Value'].mean(), label='Average Yield', color='green')
		plt.legend(bbox_to_anchor=(1,1), loc="upper left")
		plt.ylabel('Yield (bu/A)')
		plt.title('Average '+df[1]+' Yield, Mean Total Drought Time, and Mean Total Precipitation in '+state)

		plt.subplot(3, 1, 2, sharex=ax)
		plt.plot(by_year['Total Drought Time'].mean(), label='Mean Drought Time', color='red')
		plt.legend(bbox_to_anchor=(1,1), loc="upper left")
		plt.ylabel('Days in Drought')

		plt.subplot(3, 1, 3, sharex=ax)
		plt.plot(by_year['Total Precipitation'].mean(), label='Mean Total Precipitation', color='blue')
		plt.legend(bbox_to_anchor=(1,1), loc="upper left")
		plt.ylabel('Precipitation (in.)')

		plt.tight_layout()
		plt.show()



print('Data has been analyzed and plotted.')
