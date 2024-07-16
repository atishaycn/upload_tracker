import streamlit as st


def upload_ui():
    st.title("Upload Feature")

    # Category dropdown
    categories = ["Category 1", "Category 2", "Category 3"]
    category = st.selectbox("Select a category", categories)

    # Description input
    description = st.text_input("Description")

    # Amount input
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
