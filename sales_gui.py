import sys
import io
import tkinter as tk
import datetime
from tkinter import ttk
from tkcalendar import Calendar
from tkinter import messagebox
from submit_sale_handler import submit_form  # Import the submit_form function

purchase = {
    'feed': {
        'poultry': {
            'top': {'bfp': '001', 'bfm': '002', 'bssc': '003', 'bfp pro': '004', 'bssc pro': '005', 'lm': '006', 'lc': '007', 'gm': '008', 'gc': '009'},
            'chikun': {'fp': '020', 'ssp': '021', 'ufp': '022', 'ussp': '023', 'ufp plus': '024', 'ussp plus': '025', 'gp': '026', 'lm': '027', 'lc': '028'},
            'hybrid': {'fp': '030', 'ssp': '031', 'lm': '032', 'gm': '033', 'gc': '034', 'lc': '035'},
            'vital': {'fp': '040', 'ssp': '041', 'lm': '042', 'gm': '043', 'gc': '044', 'lc': '045'},
            'sunchi': {'fp': '300', 'ssp': '301', 'lm': '302', 'lc': '303', 'gm': '304', 'gp': '305'},
            'happy chicken': {'bepr': '500', 'psep': '501', 'scep': '502', 'spep': '503', 'fpap': '504', 'ber': '505', 'pse': '506', 'sce': '507', 
                              'spe': '508', 'fpe': '509', 'bcr': '510', 'bps': '511', 'bsc': '512', 'bsp': '513', 'bfp': '514', 'lcr': '515', 'lcc': '516', 'lgm': '517', 
                              'lgp': '518', 'lm1': '519', 'lm2': '520', 'lplm': '521'},
        },
        'material': {'wheat': '200', 'pkc': '201', 'soya': '202', 'gnc': '203', 'limestone': '204', 'premix': '205', 'concentrate': '206', 'Bone mill': '207', 
                     'fish mill': '208', 'maize': '209'},
        'fish': {
            'coppens': {'0.2': '090', '0.3': '091', '0.5': '092', '0.8': '093', '1.2': '094', '1.5': '095', '2': '096', '3': '097', '4': '098', '6': '099', '9': '100'},
            'top': {'2': '050', '3': '051', '4': '052', '6': '053', '9': '054'},
            'omega': {'2': '060', '3': '061', '4': '062', '6': '063', '9': '064'},
            'blue_crown': {'2': '070', '3': '071', '4': '072', '6': '073', '9': '074'},
            'eco_float': {'2': '080', '3': '081', '4': '082', '6': '083', '9': '084'},
            'vital': {'2': '400', '3': '401', '4': '402', '6': '403', '9': '404'}
        }
    }
}

current_invoice_number = None
invoice_start = None
invoice_end = None
valid_date = None

def set_invoice_range(start, end, date):
    global invoice_start, invoice_end, valid_date, current_invoice_number
    invoice_start = start
    invoice_end = end
    valid_date = date
    current_invoice_number = start
    root.deiconify()  # Show the main sales form GUI

def validate_invoice_number(invoice_number):
    if invoice_number < invoice_start or invoice_number > invoice_end:
        messagebox.showerror("Invalid Invoice Number", f"Invoice number must be between {invoice_start} and {invoice_end}")
        return False
    return True

def validate_date(sale_date):
    if sale_date != valid_date:
        messagebox.showerror("Invalid Date", f"Sale date must be {valid_date}")
        return False
    return True

def handle_form_submission():
    selected_table = table_var.get()
    if selected_table == "Choose a table":
        messagebox.showerror("Invalid Table Selection", "Please select a valid table from the dropdown menu (sales, sales_alode_ii, or sales_okrika).")
        return

    form_data = []
    for entry_set in entry_sets:
        sale_date = entry_set[0].get()
        invoice_number = int(entry_set[1].get())
        customer_id = entry_set[2].get()
        first_name = entry_set[3].get()
        last_name = entry_set[4].get()
        product_id = entry_set[5].get()
        product_name = entry_set[6].get()
        product_description = entry_set[7].get()
        sale_quantity = entry_set[8].get()
        retail_quantity = entry_set[9].get()
        unit_price = entry_set[10].get()
        result = entry_set[11].cget("text")
        cash = entry_set[12].get()
        pos = entry_set[13].get()
        bank = entry_set[14].get()
        credit = entry_set[15].get()


        if not validate_invoice_number(invoice_number) or not validate_date(sale_date):
            return

        form_data.append({
            "sale_date": sale_date,
            "invoice_number": invoice_number,
            "customer_id": customer_id,
            "first_name": first_name,
            "last_name": last_name,
            "product_id": product_id,
            "product_name": product_name,
            "product_description": product_description,
            "sale_quantity": sale_quantity,
            "retail_quantity": retail_quantity,
            "unit_price": unit_price,
            "result": result,
            "cash": cash,
            "pos": pos,
            "bank": bank,
            "credit": credit
        })


    # Format the data for confirmation message
    confirmation_message = "Are you sure you want to submit the following data?\n\n"
    for data in form_data:
        for key, value in data.items():
            confirmation_message += f"{key}: {value}\n"
        confirmation_message += "\n"

    # Display confirmation dialog
    confirm = messagebox.askyesno("Confirm Submission", confirmation_message)
    if confirm:
        # If confirmed, proceed with form submission

        # Create a StringIO buffer to capture stderr
        stderr_buffer = io.StringIO()
        old_stderr = sys.stderr
        sys.stderr = stderr_buffer

        # Call the submit_form function from submit_sale_handler
        try:
            submit_form(form_data, result_label, selected_table)
            messagebox.showinfo("Success", "Records inserted successfully!")
            #result_label.config(text="Records inserted successfully!", foreground="green")
            clear_entries()
            reset_table_menu()
        except Exception as e:
            #result_label.config(text=f"Error submitting form: {e}", foreground="red")
            #messagebox.showerror(text=f"Error submitting form: {e}", foreground="red")
            #messagebox.showerror("Error", f"Error submitting form: {e}")

            # Get the captured stderr output
            error_message = stderr_buffer.getvalue()
            
            if error_message:
                # Display the error in a messagebox
                messagebox.showerror("Error", f"An error occurred:\n{error_message}")
            else:
                messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
        finally:
            # Restore the original stderr
            sys.stderr = old_stderr
            stderr_buffer.close()

def reset_table_menu():
    table_var.set(table_options[0])  # Reset the table selection menu to the default value

def clear_entries():
    for entry_set in entry_sets:
        for i, entry in enumerate(entry_set):
            if isinstance(entry, ttk.Entry):
                entry.delete(0, tk.END)
                entry.insert(0, placeholder_texts[i-2] if i-2 < len(placeholder_texts) else "")

def open_calendar(entry):
    def on_date_select():
        selected_date = cal.get_date()
        formatted_date = datetime.datetime.strptime(selected_date, "%m/%d/%y").strftime("%Y-%m-%d")  # convert string to date object
        #formatted_date = selected_date.strftime('%Y-%m-%d')  # Format the date
        entry.delete(0, tk.END)
        entry.insert(0, formatted_date)
        top.destroy()

    top = tk.Toplevel(root)
    cal = Calendar(top, selectmode='day')
    cal.pack(padx=5, pady=5)

    select_button = ttk.Button(top, text="Select", command=on_date_select)
    select_button.pack(pady=5)

def delete_record(entry_set):
    entry_set_widgets = [widget for widget in entry_set if isinstance(widget, tk.Widget)]
    for widget in entry_set_widgets:
        widget.destroy()
    entry_sets.remove(entry_set)
    update_totals()
    reconfigure_grid()

def reconfigure_grid():
    for i, entry_set in enumerate(entry_sets, start=1):
        for widget in entry_set:
            widget.grid_configure(row=i)

def add_delete_button(entry_set):
    delete_button = ttk.Button(root, text="Drop Rec", command=lambda: delete_record(entry_set))
    delete_button.grid(row=len(entry_sets), column=17, padx=5, pady=5)
    entry_set.append(delete_button)

def add_record():

    new_entry_set = []

    # Step: Add Sale Date Entry Field and Calendar Picker
    sale_date_entry = ttk.Entry(root, width=10)  # Create sale date entry field
    sale_date_entry.insert(0, "Sale Date")  # Set placeholder text
    sale_date_entry.grid(row=len(entry_sets) + 1, column=0, padx=5, pady=5)  # Position on the grid
    sale_date_entry.bind("<Button-1>", lambda event, entry=sale_date_entry: open_calendar(entry))  # Bind left mouse button click to open calendar
    new_entry_set.append(sale_date_entry)  # Add sale date entry field to the new entry set


    # Step: Add Invoice No. Entry Field
    invoice_entry = ttk.Entry(root, width=10)  # Create invoice number entry field
    invoice_entry.insert(0, "Invoice No.")  # Set placeholder text
    invoice_entry.grid(row=len(entry_sets) + 1, column=1, padx=5, pady=5)  # Position on the grid
    new_entry_set.append(invoice_entry)  # Add invoice number entry field to the new entry set

    # Step: Add Customer ID Entry Field
    customer_id_entry = ttk.Entry(root, width=10)  # Create customer ID entry field
    customer_id_entry.insert(0, "Customer ID")  # Set placeholder text
    customer_id_entry.grid(row=len(entry_sets) + 1, column=2, padx=5, pady=5)  # Position on the grid
    new_entry_set.append(customer_id_entry)  # Add customer ID entry field to the new entry set

    # Step: Add First Name Entry Field
    first_name_entry = ttk.Entry(root, width=10)  # Create first name entry field
    first_name_entry.insert(0, "First Name")  # Set placeholder text
    first_name_entry.grid(row=len(entry_sets) + 1, column=3, padx=5, pady=5)  # Position on the grid
    new_entry_set.append(first_name_entry)  # Add first name entry field to the new entry set

    # Step: Add Last Name Entry Field
    last_name_entry = ttk.Entry(root, width=10)  # Create last name entry field
    last_name_entry.insert(0, "Last Name")  # Set placeholder text
    last_name_entry.grid(row=len(entry_sets) + 1, column=4, padx=5, pady=5)  # Position on the grid
    new_entry_set.append(last_name_entry)  # Add last name entry field to the new entry set

    # Step: Add Product ID Entry Field
    product_id_entry = ttk.Entry(root, width=10)  # Create product ID entry field
    product_id_entry.insert(0, "Product ID")  # Set placeholder text
    product_id_entry.grid(row=len(entry_sets) + 1, column=5, padx=5, pady=5)  # Position on the grid
    new_entry_set.append(product_id_entry)  # Add product ID entry field to the new entry set

    # Step: Add Product Name Entry Field
    product_name_entry = ttk.Entry(root, width=10)  # Create product name entry field
    product_name_entry.insert(0, "Product Name")  # Set placeholder text
    product_name_entry.grid(row=len(entry_sets) + 1, column=6, padx=5, pady=5)  # Position on the grid
    new_entry_set.append(product_name_entry)  # Add product name entry field to the new entry set

    # Step: Add Product Description Entry Field
    product_desc_entry = ttk.Entry(root, width=10)  # Create product description entry field
    product_desc_entry.insert(0, "Product Description")  # Set placeholder text
    product_desc_entry.grid(row=len(entry_sets) + 1, column=7, padx=5, pady=5)  # Position on the grid
    new_entry_set.append(product_desc_entry)  # Add product description entry field to the new entry set

    # Step: Add Sale Quantity Entry Field
    sale_qty_entry = ttk.Entry(root, width=10)  # Create sale quantity entry field
    sale_qty_entry.insert(0, "Sale Qty")  # Set placeholder text
    sale_qty_entry.grid(row=len(entry_sets) + 1, column=8, padx=5, pady=5)  # Position on the grid
    new_entry_set.append(sale_qty_entry)  # Add sale quantity entry field to the new entry set

    # Step: Add Retail Quantity Entry Field
    retail_qty_entry = ttk.Entry(root, width=10)  # Create retail quantity entry field
    retail_qty_entry.insert(0, "Retail Qty")  # Set placeholder text
    retail_qty_entry.grid(row=len(entry_sets) + 1, column=9, padx=5, pady=5)  # Position on the grid
    new_entry_set.append(retail_qty_entry)  # Add retail quantity entry field to the new entry set

    # Step: Add Unit Price Entry Field
    unit_price_entry = ttk.Entry(root, width=10)  # Create unit price entry field
    unit_price_entry.insert(0, "Unit Price")  # Set placeholder text
    unit_price_entry.grid(row=len(entry_sets) + 1, column=10, padx=5, pady=5)  # Position on the grid
    new_entry_set.append(unit_price_entry)  # Add unit price entry field to the new entry set

    # Step: Add Result Label
    result_label = ttk.Label(root, text="Result:")  # Create result label
    result_label.grid(row=len(entry_sets) + 1, column=11, padx=5, pady=5)  # Position on the grid
    new_entry_set.append(result_label)  # Add result label to the new entry set

    # Step: Add Cash Entry Field
    cash_entry = ttk.Entry(root, width=10)  # Create cash entry field
    cash_entry.insert(0, "Cash")  # Set placeholder text
    cash_entry.grid(row=len(entry_sets) + 1, column=12, padx=5, pady=5)  # Position on the grid
    new_entry_set.append(cash_entry)  # Add cash entry field to the new entry set

    # Step: Add POS Entry Field
    pos_entry = ttk.Entry(root, width=10)  # Create POS entry field
    pos_entry.insert(0, "POS")  # Set placeholder text
    pos_entry.grid(row=len(entry_sets) + 1, column=13, padx=5, pady=5)  # Position on the grid
    new_entry_set.append(pos_entry)  # Add POS entry field to the new entry set

    # Step: Add Bank Entry Field
    bank_entry = ttk.Entry(root, width=10)  # Create bank entry field
    bank_entry.insert(0, "Bank")  # Set placeholder text
    bank_entry.grid(row=len(entry_sets) + 1, column=14, padx=5, pady=5)  # Position on the grid
    new_entry_set.append(bank_entry)  # Add bank entry field to the new entry set

    # Step: Add Credit Entry Field
    credit_entry = ttk.Entry(root, width=10)  # Create credit entry field
    credit_entry.insert(0, "Credit")  # Set placeholder text
    credit_entry.grid(row=len(entry_sets) + 1, column=15, padx=5, pady=5)  # Position on the grid
    new_entry_set.append(credit_entry)  # Add credit entry field to the new entry set


    select_option = lambda selected_option, path: populate_product_info(new_entry_set, selected_option, path)
    select_menu(new_entry_set, select_option)

    entry_sets.append(new_entry_set)

    add_delete_button(new_entry_set)
    update_totals()
    setup_bindings(new_entry_set)
    reconfigure_grid()

def update_totals(event=None):
    total_result = sum(float(entry_set[11].cget("text")) for entry_set in entry_sets if entry_set[11].cget("text").replace('.', '', 1).isdigit())
    total_cash = sum(float(entry_set[12].get()) for entry_set in entry_sets if entry_set[12].get().replace('.', '', 1).isdigit())
    total_pos = sum(float(entry_set[13].get()) for entry_set in entry_sets if entry_set[13].get().replace('.', '', 1).isdigit())
    total_bank = sum(float(entry_set[14].get()) for entry_set in entry_sets if entry_set[14].get().replace('.', '', 1).isdigit())
    total_credit = sum(float(entry_set[15].get()) for entry_set in entry_sets if entry_set[15].get().replace('.', '', 1).isdigit())
    
    total_result_label.config(text=f"{total_result:.2f}")
    total_cash_label.config(text=f"{total_cash:.2f}")
    total_pos_label.config(text=f"{total_pos:.2f}")
    total_bank_label.config(text=f"{total_bank:.2f}")
    total_credit_label.config(text=f"{total_credit:.2f}")

def populate_product_info(new_entry_set, selected_option, path):
    new_entry_set[5].delete(0, tk.END)
    new_entry_set[5].insert(tk.END, selected_option)

    product_name = ' '.join(path[::-1][1:])
    new_entry_set[6].delete(0, tk.END)
    new_entry_set[6].insert(tk.END, product_name)

    product_description = path[-1]
    new_entry_set[7].delete(0, tk.END)
    new_entry_set[7].insert(tk.END, product_description)

def calculate_result(event=None):
    try:
        for entry_set in entry_sets:
            retail_sale_quantity = float(entry_set[9].get())
            sale_quantity = float(entry_set[8].get())
            unit_price = float(entry_set[10].get())

            if sale_quantity > 0.5 or retail_sale_quantity > 0.5:
                result = (retail_sale_quantity * unit_price) + (sale_quantity * unit_price)
            else:
                result = unit_price
            entry_set[11].config(text=f"{result}")
    except ValueError:
        entry_set[11].config(text="Invalid input")
    update_totals()

def setup_bindings(entry_set=None):
    if entry_set:
        entry_set[8].bind('<KeyRelease>', calculate_result)
        entry_set[9].bind('<KeyRelease>', calculate_result)
        entry_set[10].bind('<KeyRelease>', calculate_result)

        entry_set[11].bind('<KeyRelease>', update_totals)
        entry_set[12].bind('<KeyRelease>', update_totals)
        entry_set[13].bind('<KeyRelease>', update_totals)
        entry_set[14].bind('<KeyRelease>', update_totals)
        entry_set[15].bind('<KeyRelease>', update_totals)
    else:
        for entry_set in entry_sets:
            entry_set[8].bind('<KeyRelease>', calculate_result)
            entry_set[9].bind('<KeyRelease>', calculate_result)
            entry_set[10].bind('<KeyRelease>', calculate_result)

            entry_set[11].bind('<KeyRelease>', update_totals)
            entry_set[12].bind('<KeyRelease>', update_totals)
            entry_set[13].bind('<KeyRelease>', update_totals)
            entry_set[14].bind('<KeyRelease>', update_totals)
            entry_set[15].bind('<KeyRelease>', update_totals)
        

def select_menu(new_entry_set, select_option):
    main_menu = tk.Menu(root)
    root.config(menu=main_menu)
    build_menu(main_menu, purchase, select_option)

def build_menu(parent, options, select_option, path=[]):
    for key, value in options.items():
        new_path = path + [key]
        if isinstance(value, dict):
            submenu = tk.Menu(parent, tearoff=0)
            build_menu(submenu, value, select_option, new_path)
            parent.add_cascade(label=key, menu=submenu)
        else:
            parent.add_command(label=key, command=lambda v=value, p=new_path: select_option(v, p))

def show_range_gui():
    range_window = tk.Toplevel()
    range_window.title("Set Invoice Range and Date")

    tk.Label(range_window, text="Start Invoice Number:").grid(row=0, column=0, padx=5, pady=5)
    start_entry = ttk.Entry(range_window)
    start_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(range_window, text="End Invoice Number:").grid(row=1, column=0, padx=5, pady=5)
    end_entry = ttk.Entry(range_window)
    end_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(range_window, text="Valid Sale Date:").grid(row=2, column=0, padx=5, pady=5)
    date_entry = ttk.Entry(range_window)
    date_entry.grid(row=2, column=1, padx=5, pady=5)

    def set_range_and_date():
        start = int(start_entry.get())
        end = int(end_entry.get())
        date = date_entry.get()
        set_invoice_range(start, end, date)
        range_window.destroy()

    ttk.Button(range_window, text="Set", command=set_range_and_date).grid(row=3, columnspan=2, pady=10)

# Initialize the main Tkinter window
root = tk.Tk()
root.withdraw()  # Hide the main window initially

# Show the range and date GUI first
show_range_gui()

# Placeholder texts for the entries
placeholder_texts = ["Invoice No.", "Customer ID", "First Name", "Last Name", "Product ID",
                     "Product Name", "Product Desc", "Sale Qty", "Retail Qty", 
                     "Unit Price", "Cash", "POS", "Bank", "Credit"]

# Totals row
ttk.Label(root, text="Totals:").grid(row=0, column=10, padx=5, pady=5)

total_result_label = ttk.Label(root, text="0.00", foreground="blue")
total_result_label.grid(row=0, column=11, padx=5, pady=5)
total_cash_label = ttk.Label(root, text="0.00", foreground="blue")
total_cash_label.grid(row=0, column=12, padx=5, pady=5)
total_pos_label = ttk.Label(root, text="0.00", foreground="blue")
total_pos_label.grid(row=0, column=13, padx=5, pady=5)
total_bank_label = ttk.Label(root, text="0.00", foreground="blue")
total_bank_label.grid(row=0, column=14, padx=5, pady=5)
total_credit_label = ttk.Label(root, text="0.00", foreground="blue")
total_credit_label.grid(row=0, column=15, padx=5, pady=5)

submit_button = ttk.Button(root, text="Submit", command=handle_form_submission)
submit_button.grid(row=0, column=6, pady=10)

add_record_button = ttk.Button(root, text="Add Record", command=add_record)
add_record_button.grid(row=0, column=7, pady=10)

# Create a result label to display messages
result_label = ttk.Label(root, text="")
result_label.grid(row=0, column=8, pady=10)

# Dropdown menu for table selection
table_var = tk.StringVar(root)
table_options = ["Choose a table", "sales", "sales_alode_ii", "sales_okrika"]
table_var.set(table_options[0])  # Set default option

# Update the OptionMenu dynamically
table_menu = ttk.OptionMenu(root, table_var, table_var.get(), *table_options)
table_menu.grid(row=0, column=9, pady=10)

entry_sets = []
add_record()
setup_bindings()

root.mainloop()

