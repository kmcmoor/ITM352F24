# * For Assignment 2 Workshop, this is exercise #1
# 
#

import pandas as pd
import pyarrow #
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

#Import the data file. This needs to be downloaded to be used by Pandas.
# It is in CSV format
url = "https://drive.google.com/file/d/1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA/view?usp=sharing" #If you have trouble, delete the last part of the url, to load the file properly

#Attempt to read the CSV file
try:
    print ("Reading CSV file...")
    sales_data = pd.read_csv(url, dtype_backend='pyarrow', on_bad_lines='skip')

    #Ask Pandas to parse the order_date field into a standard representation
    #sales_data('order_date') = pd.to_datetime(sales_data['order_date'], format="mixed")

    #Save the first 10 rows of the data in sales_data_test.csv
    sales_data.head(10).to_csv('sales_data_text.csv')

except Exception as e:
    print(f"An error has occurred: {e}")