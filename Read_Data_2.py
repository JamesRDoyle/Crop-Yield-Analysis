# James Doyle
# Code to read weather data using API calls then process and export it into more usable forms


# Editable variables

# The primary directory of the overall file
base_filepath = '~/Processed_Data'

# Accepatable values in list are 'maxt', 'mint', 'avgt', 'pcpn'
# for maximum temperature, minimum temperature, average temperature, and average precipitation respectively
elems_of_interest = ['avgt', 'pcpn']


# Import needed packages
import pandas as pd 
import requests
from datetime import datetime as dt


# Create a list of all states of interest from an imported CSV (897 total)
areas_of_interest = pd.read_csv(base_filepath+'/Areas_of_Interest.csv')
states_of_interest = set(areas_of_interest['State Initial'].unique())


#---------------------------------------------------------
# Import weather data for all states and elements desired
#---------------------------------------------------------
def main():
	# For each state of interest, retrieve the weather data for the desired period
	num_errors = 0
	#states_of_interest = ['AL', 'CA', 'CO']  # TEMPORARY OBJECT ASSIGNMENT!!!!
	#states_of_interest = ['CO']  # TEMPORARY OBJECT ASSIGNMENT!!!!
	for state in states_of_interest: 
		try:
			for elem in elems_of_interest:
				make_API_call(state, elem)
		except Exception as e:
			num_errors += 1
			print("\nUnsuccessful API call for ANSI code "+state+" at "+dt.now().strftime("%I:%M%p on %d/%m/%Y"))
			print("The error was: \n" + str(e) + "\n")
		finally:
			if (num_errors >= 5):
				print("Too many unsuccessful API calls (n=5), progress has been halted")
				quit()
	print("\nAPI calls have been made with " + str(num_errors) + 
		  " total errors out of " + str(len(states_of_interest)) + " total states.")

	print("Weather data has successfully been cleaned and edited.\n")




#---------------------------------------------------------------------
# Method definition to make an API call with given State initials, 
# element desired, and optional date parameters
#---------------------------------------------------------------------
def make_API_call(state, element, sdate="1991-01-01", edate="2020-12-31"):
	elems = {}  # Serves as a parameter to the API call itself
	e_name = ''  # Later serves as the column name and part of the filename

	# Sets up the API call's elements based on this particular method call's parameters
	if (element == 'maxt'):
		elems = {"name":"maxt","interval":"dly","area_reduce":"county_max","units":"degreeF"}
		e_name = 'MaxTemp'
	elif (element == 'mint'):
		elems = {"name":"mint","interval":"dly","area_reduce":"county_min","units":"degreeF"}
		e_name = 'MinTemp'
	elif (element == 'avgt'):
		elems = {"name":"avgt","interval":"dly","area_reduce":"county_mean","units":"degreeF"}
		e_name = 'AvgTemp'
	elif (element == 'pcpn'):
		elems = {"name":"pcpn","interval":"dly","area_reduce":"county_mean","units":"inch"}
		e_name = 'AvgPrecip'
	else:
		print("\nUnnacceptable element type requested ("+element+"). Please check acceptable elements.")
		quit()


	# Make the API call using the requests package and the website's API support
	print("\nAttempting "+e_name+" API call for "+state+" at "+dt.now().strftime("%I:%M%p on %d/%m/%Y"))
	API_call = requests.post('http://data.rcc-acis.org/GridData', json=
		   {"sdate": sdate,
			"edate": edate,
			"grid":"21",
			"elems":[ elems ],
			"state": state})

	# Converts the JSON response to a Python datatype
	API_call = API_call.json()
    
	# Converts the raw Python datatype to a Pandas DataFrame
	API_call = pd.DataFrame(API_call['data'], columns=['Date', e_name])

	# Separate Dictionaries into new columns 
	# (turns each ANSI code into its own column with days as rows)
	# This long function concatenates the Date column with new columns containing the data of each ANSI code
	API_call = pd.concat([API_call.drop([e_name], axis=1), API_call[e_name].apply(pd.Series)], axis=1)


	# Delete all ANSI data columns that are not in the areas of interest
	col_interests = set(areas_of_interest['ANSI Code'].astype(str).str.zfill(5).unique())
	col_interests.add('Date')
	for column in list(API_call):  # Removes all county columns that are not of interest
		if str(column) not in col_interests:
			API_call.drop(columns=[column], inplace=True)
	del col_interests

	# Export the DataFrame to a new CSV
	API_call.to_csv(r''+base_filepath+'/Weather_Data/'+state+'_'+e_name+'.csv', index=False, header=True)
	print("Successful "+e_name+" API call for "+state+" at "+dt.now().strftime("%I:%M%p on %d/%m/%Y"))



# Run the code in the main method
main()

print('Weather data has been successfully downloaded and cleaned.')
