import json
import streamlit as st
import sys
from utils import categories, monthly_gids
from upload_test import upload_main
from tempfile import NamedTemporaryFile
from datetime import datetime

debug = len(sys.argv) > 1 and sys.argv[1] == "debug"

st.set_page_config(page_title="Upload Expenses", page_icon="💵", layout="wide")


def show_upload_input():
    st.title("Upload Feature")
    selected_sheet_options = list(monthly_gids.keys())
    selected_sheet = st.selectbox("GID:", selected_sheet_options)

    gid_input = int(monthly_gids[selected_sheet])
    # st.write(gid_input)
    category = st.selectbox("Select a category", categories)

    # Description input
    description = st.text_input("Description")

    # Amount input
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    share = st.number_input("Share", min_value=1.0, step=0.5)
    self_amount = amount / share
    st.write("Self Amount is", self_amount)
    today = datetime.today()
    formatted_date = today.strftime("%d/%m/%Y")

    data = {
        "Date": formatted_date,
        "Category": category,
        "Description": description,
        "Share": share,
        "Total Amount": amount,
        "Self Amount": self_amount,
    }
    upload_button = st.button(label="UploadB")
    if upload_button:
        upload_main(gid_input, data)


def main():
    show_upload_input()


main()
