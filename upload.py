from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
import pandas as pd
import os
import pickle
import google.auth
import streamlit as st
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import toml
from utils import sheet_id

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def get_doc_name(drive_service, doc_id):
    results = (
        drive_service.files()
        .list(pageSize=10, fields="nextPageToken, files(id, name)")
        .execute()
    )
    items = results.get("files", [])

    if not items:
        print("No files found.")
        return
    for item in items:
        if item["id"] == doc_id:
            return item["name"]


def get_sheet_name_from_gid(service, spreadsheet_id, gid):
    sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheets = sheet_metadata.get("sheets", "")
    for sheet in sheets:
        properties = sheet.get("properties", "")
        if properties.get("sheetId") == gid:
            return properties.get("title")
    return None


# def append_row_to_sheet(service, spreadsheet_id, range_name, values):
#     body = {"values": values}
#     result = (
#         service.spreadsheets()
#         .values()
#         .append(
#             spreadsheetId=spreadsheet_id,
#             range=range_name,
#             valueInputOption="RAW",
#             insertDataOption="INSERT_ROWS",
#             body=body,
#         )
#         .execute()
#     )
#     return result
def append_row_to_sheet(service, spreadsheet_id, range_name, data):
    values = [list(data.values())]
    body = {"values": values}
    result = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body=body,
        )
        .execute()
    )
    return result


def upload_main(gid_input, data):

    with open("secrets.toml", "r") as file:
        config = toml.load(file)

    google_credentials = config["google_credentials"]
    # google_credentials = st.secrets["google_credentials"]

    credentials = service_account.Credentials.from_service_account_info(
        google_credentials,
        scopes=SCOPES,
    )

    credentials.refresh(Request())

    access_token = credentials.token

    authed_session = AuthorizedSession(credentials)

    drive_service = build("drive", "v3", credentials=credentials)
    sheet_service = build("sheets", "v4", credentials=credentials)

    st.write(get_doc_name(drive_service, sheet_id))
    sheet_name = get_sheet_name_from_gid(sheet_service, sheet_id, gid_input)
    st.write(sheet_name)
    range_name = "A:F"
    if sheet_name:
        full_range = f"{sheet_name}!{range_name}"
        # new_data = "12/09/2022,Utilities,football,1,104,201,AmEx"
        # values = [new_data.split(",")]
        result = append_row_to_sheet(sheet_service, sheet_id, full_range, data)
        st.write(f"Row appended. Updated range: {result['updates']['updatedRange']}")
    # values = [new_row_data.split(",")]
    # result = append_row_to_sheet(sheets_service, spreadsheet_id, range_name, values)
    # st.write(f"Row appended. Updated range: {result['updates']['updatedRange']}")
