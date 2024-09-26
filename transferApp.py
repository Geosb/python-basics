import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
from mysql.connector import connect, Error
from tkcalendar import Calendar

class DatabaseConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return True
        except Error as e:
            # Log the error to a file or display in a messagebox for better user feedback
            print(f"Error: {e}")
            return False

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

class TransferApp:
    def __init__(self, root, db_connector, transfer_data):
        self.root = root
        self.db_connector = db_connector
        self.transfer = transfer_data

        self.create_widgets()
        self.setup_grid()

    def create_widgets(self):
        self.root.title('Grafavy - Transfer')
        self.root.iconbitmap('C:/sqlite/gui/Fish.ico')
        self.root.geometry("500x600")

        self.root.option_add('*Font', ('Helvetica', 14, 'bold'))

        self.c = self.db_connector.connection.cursor()

        self.entries = {}
        self.create_calendar_entry("Transfer Date", 0)
        self.create_entry("Transfer ID", 1)
        self.create_entry("Source Outlet ID", 2)
        self.create_entry("Destination Outlet ID", 3)
        self.create_entry("Product ID", 4) 
        self.create_entry("Product Name", 5)  
        self.create_entry("Product Description", 6)
        self.create_entry("Quantity", 7)
        self.create_entry("Notes", 8)
        
        submit_btn = tk.Button(self.root, text="Add Record to Database", command=self.confirm_insertion, font=("Helvetica", 10))
        submit_btn.grid(row=9, column=1, columnspan=1, pady=5, padx=5, ipadx=40)

        self.error_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=15, height=5, font=("Helvetica", 10))
        self.error_text.grid(row=10, column=1, columnspan=1, sticky="nsew", padx=10, pady=10)

        self.success_label = tk.Label(self.root, text='', font=("Helvetica", 10))
        self.success_label.grid(row=11, column=0, columnspan=2)

        self.product_id_var = tk.StringVar(self.root)
        self.product_id_menu = tk.OptionMenu(self.root, self.product_id_var, "")
        self.product_id_menu.grid(row=2, column=3, padx=20)

        self.populate_dropdowns()

    def setup_grid(self):
        for i in range(11):
            self.root.grid_rowconfigure(i, weight=1)
        for j in range(2):
            self.root.grid_columnconfigure(j, weight=1)

    def create_entry(self, label_text, row):
        label = tk.Label(self.root, text=label_text, font=("Helvetica", 10))
        label.grid(row=row, column=0)

        entry = tk.Entry(self.root, width=30, font=("Helvetica", 10))
        entry.grid(row=row, column=1, padx=20)

        self.entries[label_text.replace(" ", "")] = entry

    def create_calendar_entry(self, label_text, row):
        label = tk.Label(self.root, text=label_text, font=("Helvetica", 10))
        label.grid(row=row, column=0)

        entry = tk.Entry(self.root, width=30, font=("Helvetica", 10))
        entry.grid(row=row, column=1, padx=20)

        cal_button = tk.Button(self.root, text='Pick Date', command=lambda: self.pick_date(entry))
        cal_button.grid(row=row, column=3, padx=10)

        self.entries[label_text.replace(" ", "")] = entry

    def pick_date(self, entry):
        def set_date():
            entry.delete(0, tk.END)
            entry.insert(tk.END, cal.selection_get().strftime('%Y-%m-%d'))
            top.destroy()

        top = tk.Toplevel(self.root)
        cal = Calendar(top, selectmode='day', year=2024, month=3, day=1)
        cal.pack()

        ok_button = tk.Button(top, text='OK', command=set_date)
        ok_button.pack()


    def populate_dropdowns(self):
        for category1, category2_dict in self.transfer['feed'].items():
            for category2, category3_dict in category2_dict.items():
                if isinstance(category3_dict, dict):  
                    for category3, products in category3_dict.items():
                        command = lambda cat1=category1, cat2=category2, cat3=category3, prod=products: self.set_selected_values(cat1, cat2, cat3, prod)
                        self.product_id_menu['menu'].add_command(label=f"{category1} - {category2} - {category3}", command=command)

        for material, product_id in self.transfer['feed']['material'].items():
            command = lambda mat=material, prod=product_id: self.set_selected_values('material', '', mat, prod)
            self.product_id_menu['menu'].add_command(label=f"material - {material}", command=command)

    def set_selected_values(self, category1, category2, category3, product_id):        
        self.entries["ProductDescription"].delete(0, tk.END)
        self.entries["ProductDescription"].insert(tk.END, f"{category3}")

        if category1 != 'material':
            self.entries["ProductID"].delete(0, tk.END)
            self.entries["ProductID"].insert(tk.END, self.transfer['feed'][category1][category2][category3])

            self.entries["ProductName"].delete(0, tk.END)
            self.entries["ProductName"].insert(tk.END, f"{category2} {category1} feed".strip())
        else:
            self.entries["ProductID"].delete(0, tk.END)
            self.entries["ProductID"].insert(tk.END, self.transfer['feed'][category1][category3])

            self.entries["ProductName"].delete(0, tk.END)
            self.entries["ProductName"].insert(tk.END, f"{category2} {category1}".strip())

    def confirm_insertion(self):
        record_details = ""
        for key, entry in self.entries.items():
            record_details += f"{key}: {entry.get()}\n"

        confirmation_message = f"Do you want to insert this record?\n\n{record_details}"
        confirmation = messagebox.askyesno("Confirmation", confirmation_message)
        if confirmation:
            self.insert_record()
        else:
            print("Insertion aborted.")

    def insert_record(self):
        try:
            if any(not entry.get() for entry in self.entries.values()):
                raise ValueError("You have to fill in all records")

            self.c.execute("INSERT INTO transfer (TransferDate, TransferID, SourceOutletID, DestinationOutletID, ProductID, ProductName, ProductDescription, Quantity, Notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (self.entries["TransferDate"].get(), self.entries["TransferID"].get(), self.entries["SourceOutletID"].get(),
                            self.entries["DestinationOutletID"].get(), self.entries["ProductID"].get(), self.entries["ProductName"].get(),
                            self.entries["ProductDescription"].get(), self.entries["Quantity"].get(), self.entries["Notes"].get())
                                                    )

            self.db_connector.connection.commit()
            print('Record Inserted Successfully!')
            self.success_label.config(text='Record Inserted Successfully!')
            for entry in self.entries.values():
                entry.delete(0, tk.END)

        except Exception as err:
            self.error_text.delete(1.0, tk.END)  
            self.error_text.insert(tk.END, f"Error: {err}")
            print('Failed to Insert Record')
            if str(err) == "You have to fill in all records":
                self.error_text.delete(1.0, tk.END)  
                self.error_text.insert(tk.END, "Failed to insert record. You have to fill in all records")

try:
    with open("config.txt", "r") as config_file:
        lines = config_file.readlines()
        if len(lines) == 4:
            host = lines[0].strip().split("=")[1]
            user = lines[1].strip().split("=")[1]
            password = lines[2].strip().split("=")[1]
            database = lines[3].strip().split("=")[1]

            db_connector = DatabaseConnector(host, user, password, database)

            transfer = {
                'feed': {
                    'poultry': {
                        'top': {'bfp': '001', 'bfm': '002', 'bssc': '003', 'bfp pro': '004', 'bssc pro': '005', 'lm': '006', 'lc': '007', 'gm': '008', 'gc': '009'},
                        'chikun': {'fp': '020', 'ssp': '021', 'ufp': '022', 'ussp': '023', 'ufp plus': '024', 'ussp plus': '025', 'gp': '026', 'lm': '027', 'lc': '028'},
                        'hybrid': {'fp': '030', 'ssp': '031', 'lm': '032', 'gm': '033', 'gc': '034', 'lc': '035'},
                        'vital': {'fp': '040', 'ssp': '041', 'lm': '042', 'gm': '043', 'gc': '044', 'lc': '045'},
                        'sunchi': {'fp': '300', 'ssp': '301', 'lm': '302', 'lc': '303', 'gm': '304', 'gp': '305'}
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

            if not db_connector.connect():
                print("Failed to establish database connection.")
                exit()

            root = tk.Tk()
            app = TransferApp(root, db_connector, transfer)
            root.mainloop()

            db_connector.close_connection()

        else:
            print("Invalid configuration file format.")
except FileNotFoundError:
    print("Configuration file not found.")
