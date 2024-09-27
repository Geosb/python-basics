import sys
import io
import tkinter as tk
import datetime
from tkinter import ttk
from tkcalendar import Calendar
from tkinter import messagebox
from submit_purchase_handler import submit_form  # Import the submit_form function

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


# Constants and global variables
INITIAL_PURCHASE_ID = 17
current_purchase_id = INITIAL_PURCHASE_ID

# Load the purchase ID from the file
def load_purchase_id():
    global current_purchase_id
    try:
        with open('purchase_id.txt', 'r') as file:
            current_purchase_id = int(file.read().strip())
    except FileNotFoundError:
        current_purchase_id = INITIAL_PURCHASE_ID

# Save the purchase ID to the file
def save_purchase_id():
    try:
        with open('purchase_id.txt', 'w') as file:
            file.write(str(current_purchase_id))
    except Exception as e:
        print(f"Error saving purchase ID: {e}")

# Increment the purchase ID and save it
def increment_purchase_id():
    global current_purchase_id
    current_purchase_id += 1
    save_purchase_id()


def handle_form_submission():
    selected_table = table_var.get()
    if selected_table == "Choose a table":
        messagebox.showerror("Invalid Table Selection", "Please select a valid table from the dropdown menu (sales, sales_alode_ii, or sales_okrika).")
        return

    form_data = []
    for entry_set in entry_sets:
        purchase_date = entry_set[0].get()
        waybill = entry_set[1].get()
        purchase_id = int(entry_set[2].get())
        product_id = entry_set[3].get()
        product_name = entry_set[4].get()
        product_description = entry_set[5].get()
        alode_i_quantity_in = entry_set[6].get()
        alode_ii_quantity_in = entry_set[7].get()
        okrika_quantity_in = entry_set[8].get()
        carriage = entry_set[9].get()
        kg = entry_set[10].get()
        retail_opening = entry_set[11].get()
        unit_price = entry_set[12].get()
        result = entry_set[13].cget("text")


        # if not validate_invoice_number(invoice_number) or not validate_date(sale_date):
        #     return

        form_data.append({
            "purchase_date": purchase_date,
            "waybill": waybill,
            "purchase_id": purchase_id,
            "product_id": product_id,
            "product_name": product_name,
            "product_description": product_description,
            "alode_i_quantity_in": alode_i_quantity_in,
            "alode_ii_quantity_in": alode_ii_quantity_in,
            "okrika_quantity_in": okrika_quantity_in,
            "carriage": carriage,
            "kg": kg,
            "retail_opening": retail_opening,
            "unit_price": unit_price,
            "result": result

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
            clear_entries()
            reset_table_menu()
            increment_purchase_id()  # Increment purchase ID after successful submission
            initialize_purchase_id_entry()  # Reinitialize the purchase ID entry field
        except Exception as e:
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

# Initialize the purchase ID entry field
def initialize_purchase_id_entry():
    if entry_sets:
        entry_sets[0][2].delete(0, tk.END)
        entry_sets[0][2].insert(0, str(current_purchase_id))


def clear_entries():
    for entry_set in entry_sets:
        for i, entry in enumerate(entry_set):
            if isinstance(entry, ttk.Entry):
                entry.delete(0, tk.END)
                entry.insert(0, placeholder_texts[i-2] if i-2 < len(placeholder_texts) else "")

    initialize_purchase_id_entry()


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
    delete_button.grid(row=len(entry_sets), column=14, padx=5, pady=5)
    entry_set.append(delete_button)

def add_record():

    new_entry_set = []

    # Step: Add Sale Date Entry Field and Calendar Picker
    purchase_date_entry = ttk.Entry(root, width=10)  # Create sale date entry field
    purchase_date_entry.insert(0, "Purchase Date")  # Set placeholder text
    purchase_date_entry.grid(row=len(entry_sets) + 1, column=0, padx=5, pady=5)  # Position on the grid
    purchase_date_entry.bind("<Button-1>", lambda event, entry=purchase_date_entry: open_calendar(entry))  # Bind left mouse button click to open calendar
    new_entry_set.append(purchase_date_entry)  # Add sale date entry field to the new entry set

    # Step: Add waybill Entry Field
    waybill_entry = ttk.Entry(root, width=10)  # Create purchase number entry field
    waybill_entry.insert(0, "Waybill")  # Set placeholder text
    waybill_entry.grid(row=len(entry_sets) + 1, column=1, padx=5, pady=5)  # Position on the grid
    new_entry_set.append(waybill_entry)  # Add waybill entry field to the new entry set


    # Step: Add purchase date Entry Field
    purchase_entry = ttk.Entry(root, width=10)  # Create purchase number entry field
    purchase_entry.insert(0, str(current_purchase_id))  # Set placeholder text
    purchase_entry.grid(row=len(entry_sets) + 1, column=2, padx=5, pady=5)  # Position on the grid
    new_entry_set.append(purchase_entry)  # Add purchase number entry field to the new entry set

    # Step: Add Customer ID Entry Field
    product_id_entry = ttk.Entry(root, width=10)  # Create customer ID entry field
    product_id_entry.insert(0, "Product ID")  # Set placeholder text
    product_id_entry.grid(row=len(entry_sets) + 1, column=3, padx=5, pady=5)  # Position on the grid
    new_entry_set.append(product_id_entry)  # Add customer ID entry field to the new entry set

    # Step: Add Product Name Entry Field
    product_name_entry = ttk.Entry(root, width=10)  # Create first name entry field
    product_name_entry.insert(0, "Product Name")  # Set placeholder text
    product_name_entry.grid(row=len(entry_sets) + 1, column=4, padx=5, pady=5)  # Position on the grid
    new_entry_set.append(product_name_entry)  # Add first name entry field to the new entry set

    # Step: Add Product Description Entry Field
    product_description_entry = ttk.Entry(root, width=10)  # Create last name entry field
    product_description_entry.insert(0, "Product Description")  # Set placeholder text
    product_description_entry.grid(row=len(entry_sets) + 1, column=5, padx=5, pady=5)  # Position on the grid
    new_entry_set.append(product_description_entry)  # Add last name entry field to the new entry set

    # Step: Add Alode I Entry Field
    alode_i_quantity_in_entry = ttk.Entry(root, width=10)  # Create product ID entry field
    alode_i_quantity_in_entry.insert(0, "AlodeIQuantityIn ID")  # Set placeholder text
    alode_i_quantity_in_entry.grid(row=len(entry_sets) + 1, column=6, padx=5, pady=5)  # Position on the grid
    new_entry_set.append(alode_i_quantity_in_entry)  # Add product ID entry field to the new entry set

    # Step: Add Alode II Entry Field
    alode_ii_quantity_in_entry = ttk.Entry(root, width=10)  # Create product name entry field
    alode_ii_quantity_in_entry.insert(0, "AlodeIIQuantityIn")  # Set placeholder text
    alode_ii_quantity_in_entry.grid(row=len(entry_sets) + 1, column=7, padx=5, pady=5)  # Position on the grid
    new_entry_set.append(alode_ii_quantity_in_entry)  # Add product name entry field to the new entry set

    # Step: Add Okrika Entry Field
    okrika_quantity_in_entry = ttk.Entry(root, width=10)  # Create product description entry field
    okrika_quantity_in_entry.insert(0, "OkrikaQuantityIn")  # Set placeholder text
    okrika_quantity_in_entry.grid(row=len(entry_sets) + 1, column=8, padx=5, pady=5)  # Position on the grid
    new_entry_set.append(okrika_quantity_in_entry)  # Add product description entry field to the new entry set

    # Step: Add Carriage Entry Field
    carriage_entry = ttk.Entry(root, width=10)  # Create sale quantity entry field
    carriage_entry.insert(0, "Carriage")  # Set placeholder text
    carriage_entry.grid(row=len(entry_sets) + 1, column=9, padx=5, pady=5)  # Position on the grid
    new_entry_set.append(carriage_entry)  # Add sale quantity entry field to the new entry set

    # Step: Add kg Entry Field
    kg_entry = ttk.Entry(root, width=10)  # Create kg entry field
    kg_entry.insert(0, "KG")  # Set placeholder text
    kg_entry.grid(row=len(entry_sets) + 1, column=10, padx=5, pady=5)  # Position on the grid
    new_entry_set.append(kg_entry)  # Add kg entry field to the new entry set

    # Step: Add Retail Opening Entry Field
    retail_opening_entry = ttk.Entry(root, width=10)  # Create retail quantity entry field
    retail_opening_entry.insert(0, "Retail Opening")  # Set placeholder text
    retail_opening_entry.grid(row=len(entry_sets) + 1, column=11, padx=5, pady=5)  # Position on the grid
    new_entry_set.append(retail_opening_entry)  # Add retail quantity entry field to the new entry set

    # Step: Add Unit Price Entry Field
    unit_price_entry = ttk.Entry(root, width=10)  # Create unit price entry field
    unit_price_entry.insert(0, "Unit Price")  # Set placeholder text
    unit_price_entry.grid(row=len(entry_sets) + 1, column=12, padx=5, pady=5)  # Position on the grid
    new_entry_set.append(unit_price_entry)  # Add unit price entry field to the new entry set

    # Step: Add Result Label
    result_label = ttk.Label(root, text="Result:")  # Create result label
    result_label.grid(row=len(entry_sets) + 1, column=13, padx=5, pady=5)  # Position on the grid
    new_entry_set.append(result_label)  # Add result label to the new entry set



    select_option = lambda selected_option, path: populate_product_info(new_entry_set, selected_option, path)
    select_menu(new_entry_set, select_option)

    entry_sets.append(new_entry_set)

    add_delete_button(new_entry_set)
    update_totals()
    setup_bindings(new_entry_set)
    reconfigure_grid()

def update_totals(event=None):
    total_alode_i_quantity_in = sum(float(entry_set[6].get()) for entry_set in entry_sets if entry_set[6].get().replace('.', '', 1).isdigit())
    total_alode_ii_quantity_in = sum(float(entry_set[7].get()) for entry_set in entry_sets if entry_set[7].get().replace('.', '', 1).isdigit())
    total_okrika_quantity_in = sum(float(entry_set[8].get()) for entry_set in entry_sets if entry_set[8].get().replace('.', '', 1).isdigit())
    total_carriage = sum(float(entry_set[9].get()) for entry_set in entry_sets if entry_set[9].get().replace('.', '', 1).isdigit())
    total_kg = sum(float(entry_set[10].get()) for entry_set in entry_sets if entry_set[10].get().replace('.', '', 1).isdigit())
    total_retail_opening = sum(float(entry_set[11].get()) for entry_set in entry_sets if entry_set[11].get().replace('.', '', 1).isdigit())
    total_result = sum(float(entry_set[13].cget("text")) for entry_set in entry_sets if entry_set[13].cget("text").replace('.', '', 1).isdigit())
    
    total_alode_i_quantity_in_label.config(text=f"{total_alode_i_quantity_in:.2f}")
    total_alode_ii_quantity_in_label.config(text=f"{total_alode_ii_quantity_in:.2f}")
    total_okrika_quantity_in_label.config(text=f"{total_okrika_quantity_in:.2f}")
    total_carriage_label.config(text=f"{total_carriage:.2f}")
    total_kg_label.config(text=f"{total_kg:.2f}")
    total_retail_opening_label.config(text=f"{total_retail_opening:.2f}")
    total_result_label.config(text=f"{total_result:.2f}")

def populate_product_info(new_entry_set, selected_option, path):
    new_entry_set[3].delete(0, tk.END)
    new_entry_set[3].insert(tk.END, selected_option)

    product_name = ' '.join(path[::-1][1:])
    new_entry_set[4].delete(0, tk.END)
    new_entry_set[4].insert(tk.END, product_name)

    product_description = path[-1]
    new_entry_set[5].delete(0, tk.END)
    new_entry_set[5].insert(tk.END, product_description)

def calculate_result(event=None):
    try:
        for entry_set in entry_sets:
            alode_i_quantity_in = float(entry_set[6].get())
            alode_ii_quantity_in = float(entry_set[7].get())
            okrika_quantity_in = float(entry_set[8].get())
            carriage = float(entry_set[9].get())
            kg = float(entry_set[10].get())
            retail_opening = float(entry_set[11].get())
            unit_price = float(entry_set[12].get())

            if alode_i_quantity_in > 0 or alode_ii_quantity_in > 0 or okrika_quantity_in > 0:
                result = (alode_i_quantity_in * unit_price) + (alode_ii_quantity_in * unit_price) + (okrika_quantity_in * unit_price) + carriage
            elif kg > 0:
                result = unit_price / kg
            else:
                result = 0  # Set result to 0 if none of the conditions are met

            entry_set[13].config(text=f"{result:.2f}")
    except ValueError:
        for entry_set in entry_sets:
            entry_set[13].config(text="Invalid input")
    update_totals()

def setup_bindings(entry_set=None):
    if entry_set:
        entry_set[6].bind('<KeyRelease>', calculate_result)  # Alode I Quantity In
        entry_set[7].bind('<KeyRelease>', calculate_result)  # Alode II Quantity In
        entry_set[8].bind('<KeyRelease>', calculate_result)  # Okrika Quantity In
        entry_set[9].bind('<KeyRelease>', calculate_result)  # Carriage
        entry_set[10].bind('<KeyRelease>', calculate_result)  # KG
        entry_set[11].bind('<KeyRelease>', calculate_result)  # Retail Opening
        entry_set[12].bind('<KeyRelease>', calculate_result)  # Unit Price
        entry_set[13].bind('<KeyRelease>', calculate_result)  # Result
    else:
        for entry_set in entry_sets:
            entry_set[6].bind('<KeyRelease>', calculate_result)
            entry_set[7].bind('<KeyRelease>', calculate_result)
            entry_set[8].bind('<KeyRelease>', calculate_result)
            entry_set[9].bind('<KeyRelease>', calculate_result)
            entry_set[10].bind('<KeyRelease>', calculate_result)
            entry_set[11].bind('<KeyRelease>', calculate_result)
            entry_set[12].bind('<KeyRelease>', calculate_result)
            entry_set[13].bind('<KeyRelease>', calculate_result)
        

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


# Initialize the main Tkinter window
root = tk.Tk()

# Placeholder texts for the entries
placeholder_texts = ["PDate", "Waybill", "Purchase ID", "Product ID","Product Name", "Product Desc",
                     "AlodeIQtyIn", "AlodeIIQtyIn", "OkrikaQtyIn",
                      "Carriage", "KG", "Retail Opening", "Unit Price"]

# Totals row
ttk.Label(root, text="Totals:").grid(row=0, column=5, padx=5, pady=5)

total_alode_i_quantity_in_label = ttk.Label(root, text="0.00", foreground="blue")
total_alode_i_quantity_in_label.grid(row=0, column=6, padx=5, pady=5)
total_alode_ii_quantity_in_label = ttk.Label(root, text="0.00", foreground="blue")
total_alode_ii_quantity_in_label.grid(row=0, column=7, padx=5, pady=5)
total_okrika_quantity_in_label = ttk.Label(root, text="0.00", foreground="blue")
total_okrika_quantity_in_label.grid(row=0, column=8, padx=5, pady=5)
total_carriage_label = ttk.Label(root, text="0.00", foreground="blue")
total_carriage_label.grid(row=0, column=9, padx=5, pady=5)
total_kg_label = ttk.Label(root, text="0.00", foreground="blue")
total_kg_label.grid(row=0, column=10, padx=5, pady=5)
total_retail_opening_label = ttk.Label(root, text="0.00", foreground="blue")
total_retail_opening_label.grid(row=0, column=11, padx=5, pady=5)
total_result_label = ttk.Label(root, text="0.00", foreground="blue")
total_result_label.grid(row=0, column=13, padx=5, pady=5)

submit_button = ttk.Button(root, text="Submit", command=handle_form_submission)
submit_button.grid(row=0, column=2, pady=10)

add_record_button = ttk.Button(root, text="Add Record", command=add_record)
add_record_button.grid(row=0, column=3, pady=10)

# Create a result label to display messages
result_label = ttk.Label(root, text="")
result_label.grid(row=0, column=14, pady=10)

# Dropdown menu for table selection
table_var = tk.StringVar(root)
table_options = ["Choose a table", "purchase"]
table_var.set(table_options[0])  # Set default option

# Update the OptionMenu dynamically
table_menu = ttk.OptionMenu(root, table_var, table_var.get(), *table_options)
table_menu.grid(row=0, column=4, pady=10)

entry_sets = []
add_record()
setup_bindings()

# Show the main window
root.deiconify()

# Load the purchase ID at startup
load_purchase_id()

# Initialize the purchase ID entry field
initialize_purchase_id_entry()

root.mainloop()

# Initial save to create the file if it doesn't exist
save_purchase_id()