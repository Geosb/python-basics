import pandas as pd
from decimal import Decimal
import mysql.connector
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import seaborn as sns

# Function to execute a query and return the result
def execute_query(connector, query, params):
    if connector.connection:
        cursor = connector.connection.cursor()
        try:
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
        finally:
            cursor.close()
    else:
        print("Not connected to MySQL database.")

# Function to execute a query and return the result as a DataFrame
def execute_query_to_dataframe(connector, query, columns, params):
    data = execute_query(connector, query, params)
    if data:
        data_list = []
        for row in data:
            row_list = [str(cell) if isinstance(cell, Decimal) else cell for cell in row]
            data_list.append(row_list)
        
        df = pd.DataFrame(data_list, columns=columns)
        return df
    else:
        return None

# Function to plot a DataFrame (example function, adjust as needed)
def plot_dataframe(df, product_id):
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df)
    plt.title(f'Line Plot of {product_id}')
    plt.xlabel('Date')
    plt.ylabel('Sale Quantity')
    plt.show()

# Function to plot a horizontal bar chart (example function, adjust as needed)
def plot_horizontal_bar_chart(df, title):
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, orient='h')
    plt.title(title)
    plt.xlabel('Values')
    plt.ylabel('Categories')
    plt.show()

# Function to generate the report and display it in the GUI
def generate_report(df_gross_profit, df_net_profit):
    # Extracting values for each column based on entity lists
    purchase_carriage = ['', '', df_gross_profit['Purchase'][0], df_gross_profit['Carriage'][0], '', '', '', '', '', '', '', '', '', '', '', '']
    various_costs = ['', df_gross_profit['OpeningStock'][0], '', '', df_gross_profit['CostofAvailableGoods'][0], df_gross_profit['ClosingStock'][0], '', '', df_net_profit['PersonalCollection'][0], df_net_profit['Impress'][0], df_net_profit['Charges'][0], df_net_profit['Salary'][0], df_net_profit['Rent'][0], df_net_profit['InterestOnLoan'][0], df_net_profit['OtherExpenses'][0], '']
    sales_profits = [df_gross_profit['Sales'][0], '', '', '', '', '', df_gross_profit['CostofGoodsSold'][0], df_gross_profit['GrossProfit'][0], '', '', '', '', '', '', '', df_net_profit['NetProfit'][0]]

    # List of entities
    entities = [
        "Sales", "OpeningStock", "Purchase", "Carriage", "CostofAvailableGoods",
        "ClosingStock", "CostofGoodsSold", "GrossProfit", "PersonalCollection", 
        "Impress", "Charges", "Salary", "Rent", "InterestOnLoan", "OtherExpenses", 
        "NetProfit"
    ]

    # GUI setup
    root = tk.Tk()
    root.title("Financial Report")

    # Set window size
    root.geometry("800x600")

    # Add title as the only header
    title = tk.Label(root, text=f"Trading Profit & Loss for the period", font=("Helvetica", 16, "bold")) # of {df_gross_profit['GPDate'][0]}
    title.grid(row=0, column=0, columnspan=3)

    # Define the columns for the report
    columns = ["Entity", "Purchase and Carriage", "Various Costs", "Sales and Profits"]
    tree = ttk.Treeview(root, columns=columns, show="headings", height=18)

    # Define the column headings (using the title text)
    for col in columns:
        tree.heading(col, text="")

    # Set the column widths
    tree.column("Entity", width=200)
    tree.column("Purchase and Carriage", width=150)
    tree.column("Various Costs", width=150)
    tree.column("Sales and Profits", width=150)

    # Adding rows to the treeview
    for i, entity in enumerate(entities):
        tree.insert("", "end", values=(entity, purchase_carriage[i], various_costs[i], sales_profits[i]))

    # Arrange the treeview in the window
    tree.grid(row=1, column=0, columnspan=3, sticky='nsew')

    # Configure the grid to expand the treeview
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Adjust the window to fit the content
    root.update_idletasks()
    root.geometry(f"{tree.winfo_reqwidth()}x{tree.winfo_reqheight()+50}")

    # Run the GUI loop
    root.mainloop()

