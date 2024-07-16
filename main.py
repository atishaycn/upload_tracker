import json
import streamlit as st
import sys
from utils import categories
from upload_test import upload_main
from tempfile import NamedTemporaryFile

debug = len(sys.argv) > 1 and sys.argv[1] == "debug"

st.set_page_config(page_title="Upload Expenses", page_icon="💵", layout="wide")


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
    credentials_file = st.file_uploader("Upload credentials.json", type="json")
    if upload_button and credentials_file:
        credentials_json = json.load(credentials_file)
        with NamedTemporaryFile(delete=False, suffix=".json") as temp_credentials_file:
            temp_credentials_file.write(credentials_file.getbuffer())
            temp_credentials_file_path = temp_credentials_file.name
        upload_main(temp_credentials_file_path)


def main():
    show_upload_input()


main()
