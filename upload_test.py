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
    "https://www.googleapis.com/auth/drive.file",
]


def authenticate(credentials_json):
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
            flow = InstalledAppFlow.from_client_secrets_file(credentials_json, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return creds


def create_service(credentials_json):
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


def upload_main(credentials_json):
    st.write("Creating service")

    service = create_service(credentials_json)
    if service:
        spreadsheet_id = create_sheet(service, "Test Sheet")
