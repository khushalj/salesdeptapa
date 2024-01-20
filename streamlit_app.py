import streamlit as st

def main():
    st.title("A+A Sales : Pilot")

    # Menu for Party Name
    party_name = st.text_input("Party Name", "")
    st.write(f"Entered Party Name: {party_name}")

    # Menu for Address
    address = st.text_area("Address", "")
    st.write(f"Entered Address: {address}")

    # Menu for GST number
    gst_number = st.text_input("GST number", "")
    st.write(f"Entered GST number: {gst_number}")

    # Menu for Phone number
    phone_number = st.text_input("Phone number", "")
    st.write(f"Entered Phone number: {phone_number}")

if __name__ == "__main__":
    main()
