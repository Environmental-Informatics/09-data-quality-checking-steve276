#!/bin/env python
# Created on Sat Mar 21 by Miriam Stevens / @author: steve276
#
import pandas as pd
import numpy as np

def ReadData( fileName ):
    """This function takes a filename as input, and returns a dataframe with
    raw data read from that file in a Pandas DataFrame.  The DataFrame index
    should be the year, month and day of the observation.  DataFrame headers
    should be "Date", "Precip", "Max Temp", "Min Temp", "Wind Speed". Function
    returns the completed DataFrame, and a dictionary designed to contain all 
    missing value counts."""
    
    # define column names
    colNames = ['Date','Precip','Max Temp', 'Min Temp','Wind Speed']

    # open and read the file
    DataDF = pd.read_csv("DataQualityChecking.txt",header=None, names=colNames,  
                         delimiter=r"\s+",parse_dates=[0])
    DataDF = DataDF.set_index('Date')
    
    # define and initialize the missing data dictionary
    ReplacedValuesDF = pd.DataFrame(0, index=["1. No Data"], columns=colNames[1:])
     
    return( DataDF, ReplacedValuesDF )
    

def Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF ):
    """This check replaces the defined No Data value with the NumPy NaN value
    so that further analysis does not use the No Data values.  Function returns
    the modified DataFrame and a count of No Data values replaced."""

    # add your code here
    DataDF = DataDF.replace(-999, np.NaN)
    
    colNames = ['Date','Precip','Max Temp', 'Min Temp','Wind Speed']
    
    #count No Data values replaced
    ND_counts = DataDF.isna().sum()
    
    #update missing data dictionary
    ReplacedValuesDF = ReplacedValuesDF.replace( \
                         ReplacedValuesDF[colNames[1:]],
                         ND_counts[colNames[1:]] \
                         )
    
    # output checked data
    DataDF.to_csv('Checked-data.txt',header=None, sep=" ")

    return( DataDF, ReplacedValuesDF )
    
def Check02_GrossErrors( DataDF, ReplacedValuesDF ):
    """This function checks for gross errors, values well outside the expected 
    range, and removes them from the dataset.  The function returns modified 
    DataFrames with data the has passed, and counts of data that have not 
    passed the check."""
 
    # add your code here
    
    #number of Precip gross errors
    a = (len(DataDF.loc[(DataDF['Precip'] < 0)]) 
         +len(DataDF.loc[(DataDF['Precip'] > 25)]) 
        )
    
    # replace gross errors with NaN
    DataDF.loc[DataDF['Precip'] < 0, 'Precip'] = np.NaN
    DataDF.loc[DataDF['Precip'] > 25, 'Precip'] = np.NaN
    
    
    #number of Max Temp gross errors
    b = (len(DataDF.loc[(DataDF['Max Temp'] < -25)]) 
         +len(DataDF.loc[(DataDF['Max Temp'] > 35)]) 
        )
    # replace gross errors with NaN
    DataDF.loc[DataDF['Max Temp'] < -25, 'Max Temp'] = np.NaN
    DataDF.loc[DataDF['Max Temp'] > 35, 'Max Temp'] = np.NaN
    
    
    #number of Min Temp gross errors
    c = (len(DataDF.loc[(DataDF['Min Temp'] < -25)]) 
         +len(DataDF.loc[(DataDF['Min Temp'] > 35)]) 
        )
    
    # replace gross errors with NaN
    DataDF.loc[DataDF['Min Temp'] < -25, 'Min Temp'] = np.NaN
    DataDF.loc[DataDF['Min Temp'] > 35, 'Min Temp'] = np.NaN
    
    
    #number of Wind Speed gross errors
    d = (len(DataDF.loc[(DataDF['Wind Speed'] < 0)]) 
         +len(DataDF.loc[(DataDF['Wind Speed'] > 10)]) 
        )
    
    # replace gross errors with NaN
    DataDF.loc[DataDF['Wind Speed'] < 0, 'Wind Speed'] = np.NaN
    DataDF.loc[DataDF['Wind Speed'] > 10, 'Wind Speed'] = np.NaN
    
    # output checked data
    DataDF.to_csv('Checked-data.txt',header=None, sep=" ")
    
    # update missing data dictionary
    ReplacedValuesDF.loc["2. Gross Error"] = [a,b,c,d]

    return( DataDF, ReplacedValuesDF )
    
def Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture is less than
    minimum air temperature, and swaps the values when found.  The function 
    returns modified DataFrames with data that has been fixed, and with counts 
    of how many times the fix has been applied."""
    
    # add your code here
    cond = DataDF['Min Temp'] > DataDF['Max Temp']
    
    # count number of swaps needed
    num_swap = len(DataDF.loc[cond == True])
    
    # swap values
    
    
    # update missing data dictionary
    ReplacedValuesDF.loc["3. Swapped"] = [0,num_swap,num_swap,0]

    return( DataDF, ReplacedValuesDF )
    
def Check04_TmaxTminRange( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture minus 
    minimum air temperature exceeds a maximum range, and replaces both values 
    with NaNs when found.  The function returns modified DataFrames with data 
    that has been checked, and with counts of how many days of data have been 
    removed through the process."""
    
    # add your code here
    cond2 = (DataDF['Max Temp']-DataDF['Min Temp']) > 25
    
    # count number of range exceedances
    num_range_fail = len(DataDF.loc[cond2 == True])
    
    # replace temp values failing range check with NaN
    
    
    # update missing data dictionary
    ReplacedValuesDF.loc["4. Range Fail"] = [0,num_range_fail,num_range_fail,0]

    return( DataDF, ReplacedValuesDF )
    




# the following condition checks whether we are running as a script, in which 
# case run the test code, otherwise functions are being imported so do not.
# put the main routines from your code after this conditional check.

if __name__ == '__main__':

    fileName = "DataQualityChecking.txt"
    DataDF, ReplacedValuesDF = ReadData(fileName)
    
    print("\nRaw data.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF )
    
    print("\nMissing values removed.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check02_GrossErrors( DataDF, ReplacedValuesDF )
    
    print("\nCheck for gross errors complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF )
    
    print("\nCheck for swapped temperatures complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check04_TmaxTminRange( DataDF, ReplacedValuesDF )
    
    print("\nAll processing finished.....\n", DataDF.describe())
    print("\nFinal changed values counts.....\n", ReplacedValuesDF)
    
    
    # Below are the plots for before and after each data quality check
    # and write fail check summary to file
    
    # output summary of failed checks
    ReplacedValuesDF.to_csv('Fail-checks-summary.txt', sep='\t') 
    
    ReadData("DataQualityChecking.txt") 
    Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF )  
    Check02_GrossErrors( DataDF, ReplacedValuesDF )
    #Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF )
    #Check04_TmaxTminRange( DataDF, ReplacedValuesDF )
         
    
    # generate plots    
    import matplotlib.pyplot as plt
    colNames = ['Date','Precip','Max Temp', 'Min Temp','Wind Speed']

    DataDF1 = pd.read_csv("DataQualityChecking.txt",header=None, names=colNames,  
                         delimiter=r"\s+",parse_dates=[0])

    DataDF1 = DataDF1.set_index('Date')

    DataDF2 = DataDF1.replace(-999, np.NaN)

    #make 2nd plot here before DataDF2 is changed

    DataDF3 = DataDF2
    
    DataDF3.loc[DataDF3['Precip'] < 0, 'Precip'] = np.NaN
    DataDF3.loc[DataDF3['Precip'] > 25, 'Precip'] = np.NaN
    DataDF3.loc[DataDF3['Max Temp'] < -25, 'Max Temp'] = np.NaN  
    DataDF3.loc[DataDF3['Max Temp'] > 35, 'Max Temp'] = np.NaN 
    DataDF3.loc[DataDF3['Min Temp'] < -25, 'Min Temp'] = np.NaN
    DataDF3.loc[DataDF3['Min Temp'] > 35, 'Min Temp'] = np.NaN
    DataDF3.loc[DataDF3['Wind Speed'] < 0, 'Wind Speed'] = np.NaN
    DataDF3.loc[DataDF3['Wind Speed'] > 10, 'Wind Speed'] = np.NaN  

    x = DataDF1.index 

    # Precipitation Plot
    fig, (ax1,ax2) = plt.subplots(nrows=2,ncols=1)
    fig.suptitle('Precipitation (mm)')

    ax1.plot(x, DataDF1['Precip'], 'k', label="Before no data & gross error check")
    ax1.set_xticklabels([])
    ax1.legend(loc='upper center', bbox_to_anchor=(0.5,-1.5))

    ax2.plot(x, DataDF3['Precip'], 'r', label="After check")
    ax2.set_xlabel('Date')
    ax2.set_xticklabels(['','1915-03','','','','1916-03','','','1916-12'])
    ax2.legend(loc='upper center', bbox_to_anchor=(0.5,-0.5))

    plt.savefig('Precipitation-Before-After.pdf', bbox_inches='tight')


    # Wind Speed Plot
    fig, (ax1,ax2) = plt.subplots(nrows=2,ncols=1)
    fig.suptitle('Wind Speed (m/s)')

    ax1.plot(x, DataDF1['Wind Speed'], 'k', label="Before check")
    ax1.set_xticklabels([])
    ax1.legend(loc='upper center', bbox_to_anchor=(0.5,-1.5))

    ax2.plot(x, DataDF3['Wind Speed'], 'r', label="After check")
    ax2.set_xlabel('Date')
    ax2.set_xticklabels(['','1915-03','','','','1916-03','','','1916-12'])
    ax2.legend(loc='upper center', bbox_to_anchor=(0.5,-0.5))

    plt.savefig('Wind-speed_Before-After.pdf', bbox_inches='tight')


    #DataDF4 =

    #DataDF5 = 
    
 
    