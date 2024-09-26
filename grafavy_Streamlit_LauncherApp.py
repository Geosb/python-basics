import streamlit as st
import subprocess
import datetime

# Function to get the greeting message
def get_greeting_message():
    current_hour = datetime.datetime.now().hour
    if current_hour < 12:
        greeting = "Good morning"
    elif 12 <= current_hour < 18:
        greeting = "Good day"
    else:
        greeting = "Good evening"
    message = f"😄 Hello sunshine, {greeting}.\n\nPlease, ensure to key in all Purchases and Retail Openings for the day before attempting sales.\n\nHappy data entry!"
    return message

# Main function for the Streamlit app
def main():
    st.title("Greeting")
    st.write(get_greeting_message())

    if st.button("OK"):
        st.experimental_rerun()

# Main App interface
def main_app():
    st.title("Grafavy Interface Launcher")
    st.sidebar.title("Menu")
    
    section = st.sidebar.selectbox("Choose Section", ["Record Entry", "Record Check", "Record Update", "Record Analysis"])

    if section == "Record Entry":
        st.header("Record Entry")
        if st.button("Purchase"):
            subprocess.Popen(["py", "purchase_gui_v2.3.py"])
        if st.button("Sales GUI"):
            subprocess.Popen(["py", "sales_gui.py"])
        if st.button("Transfer"):
            subprocess.Popen(["py", "transferApp.py"])
        if st.button("Transaction"):
            subprocess.Popen(["py", "transactionApp.py"])
        if st.button("Expenses"):
            subprocess.Popen(["py", "expenses.py"])

    elif section == "Record Check":
        st.header("Record Check")
        if st.button("Confirm Sale"):
            subprocess.Popen(["py", "confirm_sale.py"])
        if st.button("Cummulative Sale"):
            subprocess.Popen(["py", "Cummulative_sale.py"])
        if st.button("Stock Record"):
            subprocess.Popen(["py", "confirm_stockrecord.py"])
        if st.button("Stock Valuation Record"):
            subprocess.Popen(["py", "confirm_stockvaluation.py"])
        if st.button("Cumm Brand Value"):
            subprocess.Popen(["py", "brand_cumm.py"])
        if st.button("StockValue by Brand"):
            subprocess.Popen(["py", "brand_stockvalue.py"])
        if st.button("Gross Profit Record"):
            subprocess.Popen(["py", "confirm_grossprofit.py"])

    elif section == "Record Update":
        st.header("Record Update")
        if st.button("Update Sale"):
            subprocess.Popen(["py", "update_sale.py"])
        if st.button("Update Stockrecord"):
            subprocess.Popen(["py", "update_stockrecord.py"])
        if st.button("Update Stock Value"):
            subprocess.Popen(["py", "update_stockvaluation.py"])

    elif section == "Record Analysis":
        st.header("Record Analysis")
        if st.button("Product Analysis"):
            subprocess.Popen(["py", "product_performance.py"])
        if st.button("Top 20 Products"):
            subprocess.Popen(["py", "top20.py"])
        if st.button("Bottom 20 Products"):
            subprocess.Popen(["py", "bottom20.py"])
        if st.button("Top Retail Product"):
            subprocess.Popen(["py", "top20Retail.py"])
        if st.button("Bag vs Retail"):
            subprocess.Popen(["py", "compare.py"])
        if st.button("TPL A"):
            subprocess.Popen(["py", "tpl.py"])
        if st.button("Cumm TPL"):
            subprocess.Popen(["py", "cumm_tpl.py"])

# Choose to display the greeting or main app based on session state
if "show_main_app" not in st.session_state:
    st.session_state["show_main_app"] = False

if not st.session_state["show_main_app"]:
    main()
    if st.button("Proceed"):
        st.session_state["show_main_app"] = True
        st.experimental_rerun()
else:
    main_app()
