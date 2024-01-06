import streamlit as st
import gspread
from gspread_dataframe import set_with_dataframe
import pandas as pd
from PIL import Image
from io import BytesIO
from datetime import datetime

# Connect to Google Sheets (replace 'your-google-sheets-credentials.json' with your actual credentials file)
gc = gspread.service_account(filename='your-google-sheets-credentials.json')
spreadsheet_key = 'your-spreadsheet-key'
worksheet_name = 'Orders'
worksheet = gc.open_by_key(spreadsheet_key).worksheet(worksheet_name)

# Streamlit App
st.title("Box Factory Order Management")

# Sidebar for entering order details
st.sidebar.header("Add New Order")

# Collect order details
party_name = st.sidebar.text_input("Party Name")
phone_number = st.sidebar.text_input("Phone Number")
address = st.sidebar.text_area("Address")
gstin = st.sidebar.text_input("GSTIN")
ply = st.sidebar.text_input("PLY")
length = st.sidebar.number_input("Length")
width = st.sidebar.number_input("Width")
height = st.sidebar.number_input("Height")
quantity = st.sidebar.number_input("Quantity", min_value=1)
date = st.sidebar.date_input("Date", datetime.today())
print_preference = st.sidebar.selectbox("Print Preference", ["Yes", "No"])
notes = st.sidebar.text_area("Notes")

# Image upload option
image_upload = st.sidebar.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

# Signature field
signature = st.sidebar.canvas_drawing(
    key="signature",
    width=300,
    height=100,
    drawing_mode="freedraw",
    key_up_hook=lambda e: st.sidebar.markdown("### Signature Captured!"),
)

# Timestamp
timestamp = datetime.now()

# Submit button
submit_button = st.sidebar.button("Submit Order")

# Store the order details in Google Sheets
if submit_button:
    order_data = {
        "Party Name": party_name,
        "Phone Number": phone_number,
        "Address": address,
        "GSTIN": gstin,
        "PLY": ply,
        "Length": length,
        "Width": width,
        "Height": height,
        "Quantity": quantity,
        "Date": date,
        "Print Preference": print_preference,
        "Notes": notes,
        "Timestamp": timestamp,
    }

    # Convert signature to an image
    if signature:
        signature_image = Image.fromarray(signature.image_data)
        signature_image_bytes = BytesIO()
        signature_image.save(signature_image_bytes, format="PNG")
        order_data["Signature"] = signature_image_bytes.getvalue()

    # Upload image to Google Sheets
    if image_upload:
        order_data["Image Upload"] = image_upload.read()

    # Append data to Google Sheets
    existing_data = worksheet.get_all_records()
    df = pd.DataFrame(existing_data)
    df = df.append(order_data, ignore_index=True)
    set_with_dataframe(worksheet, df, include_index=False)

    st.sidebar.success("Order Submitted Successfully!")

# Display order details in the main section
st.header("Current Orders")
current_orders = worksheet.get_all_records()
st.write(pd.DataFrame(current_orders))

# Additional features, data validation, and error handling can be added based on your specific requirements.
