# Instructions:
# Build a dashboard that analyzes sales data that:
# R1: Loads the sales data file appropriately 
# R2: Displays 10 options on how the user wants to view the data
# R3: Creates pivot tables for this data
# R4: For option #9, allows the user to create their own pivot table - viewing the data however they want to
# IR 1: For each result, ask the user if they want the results exported to an Excel file (that can be read directly into Excel). Ask the user what filename they want.
# IR 2: When the sales data is loaded, display a summary of the data (total orders, number of employees, sales regions, dates range of orders, number of unique customers, product categories, unique states, total sales amount, total quantities of products sold). If some data is not available (missing columns) for a pre-defined analytic, remove that analytic from the menu options.



#R1
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
            print(f"All required columns are present\n\n* Note: Some fields may be missing and some analytics may not work")

        # Ask Pandas to parse the order_date field into a standard representation
        sales_data['order_date'] = pd.to_datetime(sales_data['order_date'], format="mixed")

        # Replace any missing data with zeros - looked this up on google!
        sales_data = sales_data.fillna(0)

        # Save the first 10 rows of the data in sales_data_test.csv
        sales_data.head(10).to_csv('sales_data_test.csv')
        display_summary(sales_data)

        return sales_data
    
    except FileNotFoundError:
        print(f"Error: the file {file_path} was not found.")
    except pd.errors.EmptyDataError as e:
        print(f"Error: the file {file_path} was empty.")
    except pd.errors.ParserError as e:
        print(f"Error: there was a problem parsing {file_path}.")
    except Exception as e:
        print(f"An unexpected error has occurred: {e}")



#IR2
# Display a summary of data. Used Claude for help on how to do this
def display_summary(data):
    print("\nSummary of Sales Data")
    data_summary = {
        'Total Orders': None, 
        'Number of Employees': 'employee_id',
        'Sales Regions': 'sales_region',
        'Date Range': 'order_date',
        'Unique Customers': 'customer_id',
        'Product Categories': 'product_category',
        'Unique States': 'customer_state',
        'Total Sales Amount': 'unit_price',
        'Total Products Sold': 'quantity'
    }
    
    # Print a description of each data
    for description, required_column in data_summary.items():
        try:
            if required_column is None:
                print(f"{description}: {len(data)}")
            
            elif required_column in data.columns:
                if required_column == 'order_date':
                    earliest_date = data['order_date'].min()
                    latest_date = data['order_date'].max()
                    print(f"{description}: {earliest_date.date()} to {latest_date.date()}")
                
                elif description == 'Number of Employees':
                    print(f"{description}: {data['employee_id'].nunique()}")
                
                elif description == 'Sales Regions':
                    regions = data['sales_region'].unique()
                    print(f"{description}: {', '.join(regions)}")
                
                elif description == 'Product Categories':
                    categories = data['product_category'].unique()
                    print(f"{description}: {', '.join(categories)}")
                
                elif description == 'Unique States':
                    states = data['customer_state'].unique()
                    print(f"{description}: {', '.join(states)}")
                
                elif description == 'Unique Customers':
                    print(f"{description}: {data['customer_id'].nunique()}")
                
                elif description == 'Total Sales Amount':
                    total_sales = data['unit_price'].sum()
                    print(f"{description}: ${total_sales:,.2f}")
                
                elif description == 'Total Products Sold':
                    print(f"{description}: {data['quantity'].sum():,}")
            
            else:
                print(f"{description}: Data not available (missing {required_column} column)")
                
                # If some data is not available (missing columns) for a pre-defined analytic, remove that analytic from the menu options
                if description == 'Number of Employees' and 'employees_by_region' in globals():
                    menu_options = [opt for opt in menu_options if opt[1] != employees_by_region]
                    
        except Exception as e:
            print(f"{description}: Unable to calculate ({str(e)})")



#R2
# Display the top-level menu of user options
def display_menu(data):
    menu_options = (
        ("Show the first n rows of sales data", display_rows),
        ("Total sales by region and order type", sales_by_region),
        ("Average sales by region with average sales by state and sale type", avgsales_by_state),
        ("Sales by customer type and order type by state", sales_by_state),
        ("Total sales quantity and price by region and product", sales_by_product),
        ("Total sales quantity and price customer type", sales_by_order),
        ("Max and min sales price of sales by category", sales_by_category),
        ("Number of unique employees by region", employees_by_region),
        ("Create a custom pivot table", custom_pivot_table),
        ("Exit", exit_program)
    )
    print("\n--- Sales Data Dashboard ---")
    for index, (description, _) in enumerate(menu_options):
        print(f"{index+1}: {description}")

    num_choices = len(menu_options)
    choice = int(input(f"Select an option between 1 and {num_choices}: "))

    if 1 <= choice <= num_choices:
        action = menu_options[choice-1][1]
        action(data)
    else:
        print("Invalid input. Please re-enter.")



#IR1
# Ask the user if they want to export their pivot table to an excel file
def export_to_excel(df):
    while True:
        export_choice = input("\nDo you want to export this pivot table to an Excel file?\nType 'Yes' or 'No': ").strip().lower()
        
        if export_choice == 'yes':
            filename = input("Enter the filename: ").strip()
            if not filename.endswith('.xlsx'): # Used Claude for help with how to add '.xlsx' to the end of the user's filename
                filename += '.xlsx'

            try:
                df.to_excel(filename, index=True)
                print(f"Results exported to {filename}")
                break
            except Exception as e:
                print(f"Error exporting to Excel: {e}")
            break
        elif export_choice == 'no':
            print("Results not exported.")
            break
        else:
            print("Invalid input. Please type 'Yes' or 'No'.")



#R3
# (Option #1) Function to display a user-choosable number of rows
def display_rows(data):
    while True:
        numRows = len(data) - 1
        print("\nEnter rows to display:")
        print(f"- Enter a number between 1 and {numRows}")
        print("- To see all rows, enter 'all'")
        print("- To skip preview, press Enter")
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
    export_to_excel(salespivot)
    return salespivot

# (Option #3) Print average sales by state and columns being order type 
def avgsales_by_state(data):
    avgsalespivot = pd.pivot_table(data, values="unit_price", index="customer_state", columns="order_type",
    aggfunc="mean"
    )
    print("\nAverage Sales by State and Order Type\n")
    print(avgsalespivot)
    export_to_excel(avgsalespivot)
    return avgsalespivot

# (Option #4) Print total sales by state and columns being customer type and order type 
def sales_by_state(data):
    salesbystatepivot = pd.pivot_table(data, values="unit_price", index="customer_state", columns=["customer_type", "order_type"],
    aggfunc="sum", margins=True, margins_name="Totals"
    )
    print("\nSales by Customer Type and Order Type by State\n")
    print(salesbystatepivot)
    export_to_excel(salesbystatepivot)
    return salesbystatepivot

# (Option #5) Print total sales by region and product and columns being quantity and sales price 
def sales_by_product(data):
    salesbyproductpivot = pd.pivot_table(data, values="unit_price", index=["sales_region", "quantity"], columns=["product_category"], 
    aggfunc="sum", margins=True, margins_name="Totals"
    )
    print("\nTotal Sales Quantity and Price by Region and Product\n")
    print(salesbyproductpivot)
    export_to_excel(salesbyproductpivot)
    return salesbyproductpivot

# (Option #6) Print total sales by order and customer type and columns being quantity and sales price
def sales_by_order(data):
    salesbyorderpivot = pd.pivot_table(data, values="unit_price", index=["quantity"], columns=["order_type", "customer_type"], 
    aggfunc="sum", margins=True, margins_name="Totals"
    )
    print("\nTotal Sales Quantity and Price Customer Type\n")
    print(salesbyorderpivot)
    export_to_excel(salesbyorderpivot)
    return salesbyorderpivot

# (Option #7) Print sales by category and shows the max and min sales price per row 
def sales_by_category(data):
    salesbycategorypivot = pd.pivot_table(data, values="unit_price", index=["product_category"], 
    aggfunc=["max", "min"]
    )
    print("\nSales By Category and the Max and Min Sales Price Per Row\n")
    print(salesbycategorypivot)
    export_to_excel(salesbycategorypivot)
    return salesbycategorypivot

# (Option #8) Print the number of unique employees per region
def employees_by_region(data):
    employeespivot = pd.pivot_table(data, index="sales_region", values="employee_id",
                                 aggfunc=pd.Series.nunique)
    print("\nNumber of Employees by Region")
    employeespivot.columns = ['Number of Employees']  # Rename the column for readability
    print(employeespivot)
    export_to_excel(employeespivot)
    return employeespivot

# (Option #10) Cleanly exit the program
def exit_program(data):
    sys.exit(0)    



#R4
# (Option #9) Create a custom pivot table
def custom_pivot_table(data):
    # Rows 
    print("\nSelect rows:")
    row_options = [
        'employee_name', 
        'sales_region', 
        'product_category'
    ]
    
    for index, option in enumerate(row_options, start=1):
        print(f"{index}: {option}")
    
    row_choice = input("Enter the number(s) of your choice(s), separated by commas: ").strip()
    selected_rows = [     # Used ChatGPT for help on how to read the user's input, also used this code as a reference for the selected_columns, selected_values, and selected_aggfucs sections. I used the prompt "im doing my coding assignment and im stuck on one part of the code. these are the instructions for this section of my code: (pasted instructions), and this is how my code is looking so far: (pasted code), how do i write code to read the user's input?"
        row_options[int(num.strip()) - 1]
        for num in row_choice.split(',')
        if num.strip().isdigit() and 1 <= int(num.strip()) <= len(row_options)
    ]

    if not selected_rows:
        print("No valid row selected, please try again.")
        return

    # Columns 
    print("\nSelect columns (optional):")
    column_options = [
        'order_type', 
        'customer_type'
    ]
    
    for index, option in enumerate(column_options, start=1):
        print(f"{index}: {option}")
    
    column_choice = input("Enter the number(s) of your choice(s), separated by commas (enter for no grouping): ").strip()
    selected_columns = [
        column_options[int(num.strip()) - 1] 
        for num in column_choice.split(',')
        if num.strip().isdigit() and 1 <= int(num.strip()) <= len(column_options)
    ]
    
    # Values 
    print("\nSelect values:")
    value_options = [
        'quantity', 
        'sale_price'
    ]
    
    for index, option in enumerate(value_options, start=1):
        print(f"{index}: {option}")
    
    value_choice = input("Enter the number(s) of your choice(s), separated by commas: ").strip()
    selected_values = [
        value_options[int(num.strip()) - 1]  
        for num in value_choice.split(',')
        if num.strip().isdigit() and 1 <= int(num.strip()) <= len(value_options)
    ]

    if not selected_values:
        print("No valid value selected, please try again.")
        return

    # Aggregation function 
    print("\nSelect aggregation function:")
    agg_options = [
        'sum', 
        'mean', 
        'count'
    ]
    
    for index, option in enumerate(agg_options, start=1):
        print(f"{index}: {option}")
    
    agg_choice = input("Enter the number(s) of your choice(s), separated by commas: ").strip()
    selected_aggfuncs = [
        agg_options[int(num.strip()) - 1]  
        for num in agg_choice.split(',')
        if num.strip().isdigit() and 1 <= int(num.strip()) <= len(agg_options)
    ]

    if not selected_aggfuncs:
        print("No valid aggregation function selected, please try again.")
        return

    # Generate the pivot table
    print("\nGenerating your custom pivot table...\n")
    for aggfunc in selected_aggfuncs:
        try:
            custom_pivot = pd.pivot_table(
                data, 
                values=selected_values, 
                index=selected_rows, 
                columns=selected_columns if selected_columns else None,  
                aggfunc=aggfunc,
                margins=True, 
                margins_name="Total"  
            )
            print(f"\nCustom Pivot Table\n")
            print(custom_pivot)
            export_to_excel(custom_pivot)
        except Exception as e:
            print(f"Error creating the pivot table: {e}")

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