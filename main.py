import json
import streamlit as st
import sys
from utils import categories, monthly_gids
from upload import upload_main
from tempfile import NamedTemporaryFile
from datetime import datetime

debug = len(sys.argv) > 1 and sys.argv[1] == "debug"

st.set_page_config(page_title="Upload Expenses", page_icon="💵", layout="wide")


def show_upload_input():
    st.title("Upload Feature")
    selected_sheet_options = list(monthly_gids.keys())
    selected_sheet = st.selectbox("GID:", selected_sheet_options)

    gid_input = int(monthly_gids[selected_sheet])
    category = st.selectbox("Select a category", categories)

    description = st.text_input("Description")
    amount = float(st.text_input("Amount", value=0))
    share = float(st.text_input("Share", value=1))
    self_amount = round(amount / share, 2)
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
    upload_button = st.button(label="Upload")
    if upload_button:
        upload_main(gid_input, data)


def main():
    show_upload_input()


main()
