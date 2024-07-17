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

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def authenticate(credentials_json):
    st.write("read flow")
    creds = None
    # Check if token.pickle file exists
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            st.write("starting flow")
            flow = InstalledAppFlow.from_client_secrets_file(credentials_json, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return creds


def create_service(credentials_json):
    st.write("authenticate")
    creds = authenticate(credentials_json)
    try:
        service = build("sheets", "v4", credentials=creds)
        return service
    except HttpError as err:
        print(err)
        return None


def create_sheet(service, title):
    sheet = {"properties": {"title": title}}
    spreadsheet = (
        service.spreadsheets().create(body=sheet, fields="spreadsheetId").execute()
    )
    print(f'Spreadsheet ID: {spreadsheet.get("spreadsheetId")}')
    return spreadsheet.get("spreadsheetId")


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


import json
import toml


def upload_main():
    # config = st.secrets["google_credentials"]
    google_credentials = st.secrets["google_credentials"]

    # Load the credentials from the dictionary
    credentials = service_account.Credentials.from_service_account_info(
        google_credentials,
        scopes=SCOPES,
    )

    credentials.refresh(Request())

    access_token = credentials.token

    authed_session = AuthorizedSession(credentials)

    drive_service = build("drive", "v3", credentials=credentials)
    sheet_service = build("sheets", "v4", credentials=credentials)

    st.write(
        get_doc_name(drive_service, "1SCx92DH3-EUUJ0M7EcOlfqJ5LmOXPUh7CeZQ3hx4s14")
    )
    # service = create_service(credentials_json)
    # st.write("service created")
    # if service:
    # spreadsheet_id = create_sheet(service, "Test Sheet")
