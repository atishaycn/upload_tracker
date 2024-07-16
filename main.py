import streamlit as st
import sys
from utils import categories
from upload_test import upload_main

debug = len(sys.argv) > 1 and sys.argv[1] == "debug"

st.set_page_config(page_title="Financial Upload", page_icon="💵", layout="wide")


def show_upload_input():
    st.title("Upload Feature")

    # Category dropdown
    category = st.selectbox("Select a category", categories)

    # Description input
    description = st.text_input("Description")

    # Amount input
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    share = st.number_input("Share", min_value=1.0, step=0.5)
    self_amount = amount / share
    st.write("Self Amount is", self_amount)
    data = {
        "Category": category,
        "Description": description,
        "Total Amount": amount,
        "Share": share,
        "Self Amount": self_amount,
    }
    upload_button = st.button(label="Upload")
    if upload_button:
        upload_main()


def main():
    show_upload_input()


main()
