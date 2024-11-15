# Instructions:
# Build a dashboard that analyzes sales data that:
# 1. Loads the sales data file appropriately 
# 2. Displays 10 options on how the user wants to view the data
# 3. Creates pivot tables for this data
# 4. Allows the user to create their own pivot table - viewing the data however they want to

import pandas as pd
import pyarrow  
import ssl
import time
import sys

ssl._create_default_https_context = ssl._create_unverified_context

# Set the display to show all columns
#pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)


# Import the data file.  This needs to be downloaded to be used by Pandas.  
# It is in CSV format.
def load_csv(file_path):
    # Attempt to read the CSV file  
    try:
        print(f"Reading CSV file: {file_path}")
        start_time = time.time()
        sales_data = pd.read_csv(file_path, dtype_backend='pyarrow', on_bad_lines="skip")
        load_time = time.time() - start_time  
        print(f"File loaded in {load_time:.2f} seconds")
        print(f"Number of rows: {len(sales_data)}")
        #print(f"Columns: {sales_data.columns.to_list()}")

        # List the required columns
        required_columns = ['quantity', 'order_date', 'unit_price']

        # Check for missing columns
        missing_columns = [col for col in required_columns if col not in sales_data.columns]

        if missing_columns:
            print(f"\nWarning: The following required columns are missing: {missing_columns} ")
        else:
            print(f"\nAll required columns are present")

        # Ask Pandas to parse the order_date field into a standard representation
        sales_data['order_date'] = pd.to_datetime(sales_data['order_date'], format="mixed")

        # Save the first 10 rows of the data in sales_data_test.csv
        sales_data.head(10).to_csv('sales_data_test.csv')

        return sales_data

    except FileNotFoundError:
        print(f"Error: the file {file_path} was not found.")
    except pd.errors.EmptyDataError as e:
        print(f"Error: the file {file_path} was empty.")
    except pd.errors.ParserError as e:
        print(f"Error: there was a problem parsing {file_path}.")
    except Exception as e:
        print(f"An unexpected error has occurred: {e}")

# Display the top-level menu of user options
def display_menu(data):
    menu_options = (
        ("Show the first n rows of data", display_rows),
        ("Show total sales by region and order type", sales_by_region),
        ("Show average sales by region with average sales by state and sale type", avgsales_by_state),
        ("Show sales by customer type and order type by state", sales_by_state),
        ("Show total sales quantity and price by region and product", sales_by_product),
        ("Show total sales quantity  and price customer type", sales_by_order),
        ("Show sales by category and the max and min sales price per row", sales_by_category),
        ("Show the number of employees by region", employees_by_region),
        ("Exit the program", exit_program)
    )
    print("\nPlease choose from among these options:")
    for index, (description, _) in enumerate(menu_options):
        print(f"{index+1}: {description}")

    num_choices = len(menu_options)
    choice = int(input(f"Select an option between 1 and {num_choices}: "))

    if 1 <= choice <= num_choices:
        action = menu_options[choice-1][1]
        action(data)
    else:
        print("Invalid input. Please re-enter.")

# (Option #1) Function to display a user-choosable number of rows
def display_rows(data):
    while True:
        numRows = len(data) - 1
        print("\nEnter number of rows to display:")
        print(f"- Enter a number between 1 and {numRows}")
        print("- To see all rows enter 'all'")
        print("- To skip, press Enter")
        user_choice = input("Your choice: ").strip().lower()

        if user_choice == '':
            print("Skipping preview")
            break
        elif user_choice == 'all':
            print(data)
            break
        elif user_choice.isdigit() and 1 <= int(user_choice) <= numRows:
            print(data.head(int(user_choice)))
            break
        else:
            print("Invalid input. Please re-enter.")

# (Option #2) Print total sales by region and columns being order type
def sales_by_region(data):
    salespivot = pd.pivot_table(data, values="unit_price", index="sales_region", columns="order_type",
    aggfunc="sum", margins=True, margins_name="Totals"
    )
    print("\nTotal Sales by Region and Order Type\n")
    print(salespivot)
    return salespivot

# (Option #3) Print average sales by state and columns being order type 
def avgsales_by_state(data):
    avgsalespivot = pd.pivot_table(data, values="unit_price", index="customer_state", columns="order_type",
    aggfunc="mean"
    )
    print("\nAverage Sales by State and Order Type\n")
    print(avgsalespivot)
    return avgsalespivot

# (Option #4) Print total sales by state and columns being customer type and order type 
def sales_by_state(data):
    salesbystatepivot = pd.pivot_table(data, values="unit_price", index="customer_state", columns=["customer_type", "order_type"],
    aggfunc="sum", margins=True, margins_name="Totals"
    )
    print("\nSales by Customer Type and Order Type by State\n")
    print(salesbystatepivot)
    return salesbystatepivot

# (Option #5) Print total sales by region and product and columns being quantity and sales price 
def sales_by_product(data):
    salesbyproductpivot = pd.pivot_table(data, values="unit_price", index=["sales_region", "quantity"], columns=["product_category"], 
    aggfunc="sum", margins=True, margins_name="Totals"
    )
    print("\nTotal Sales Quantity and Price by Region and Product\n")
    print(salesbyproductpivot)
    return salesbyproductpivot

# (Option #6) Print total sales by order and customer type and columns being quantity and sales price
def sales_by_order(data):
    salesbyorderpivot = pd.pivot_table(data, values="unit_price", index=["quantity"], columns=["order_type", "customer_type"], 
    aggfunc="sum", margins=True, margins_name="Totals"
    )
    print("\nTotal Sales Quantity and Price Customer Type\n")
    print(salesbyorderpivot)
    return salesbyorderpivot

# (Option #7) Print sales by category and shows the max and min sales price per row 
def sales_by_category(data):
    salesbycategorypivot = pd.pivot_table(data, values="unit_price", index=["product_category"], 
    aggfunc=["max", "min"]
    )
    print("\nSales By Category and the Max and Min Sales Price Per Row\n")
    print(salesbycategorypivot)
    return salesbycategorypivot

# (Option #8) Print the number of unique employees per region
def employees_by_region(data):
    employeespivot = pd.pivot_table(data, index="sales_region", values="employee_id",
                                 aggfunc=pd.Series.nunique)
    print("\nNumber of Employees by Region")
    employeespivot.columns = ['Number of Employees']  # Rename the column for readability
    print(employeespivot)
    return employeespivot

# (Option #9) Create a custom pivot table
# Need help here!

# (Option #10) Cleanly exit the program
def exit_program(data):
    sys.exit(0)    

# Call load_csv to load the file
url = "https://drive.google.com/uc?export=download&id=1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA"
sales_data = load_csv(url)

# Main loop for user interaction
def main():
    while True:
        display_menu(sales_data)

# If this is the main program, call main()
if __name__ == "__main__":
    main()