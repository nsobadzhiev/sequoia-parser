import csv
import os

from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def read_data_from_spreadsheet(
        spreadsheet_id: str,
        sheet_name: str,
        replace_range: str,
        credentials_file_path: str = 'sheets_credentials.json'
):
    """
    Reads a specified range from a spreadsheet
    :param spreadsheet_id: id of the spreadsheet
    :param sheet_name: name of the sheet within the document
    :param replace_range: range to read (e.g. A1:E4)
    :param credentials_file_path: path to the Google cloud credentials
    """

    # Create a Sheets API instance
    credentials = service_account.Credentials.from_service_account_file(credentials_file_path, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()

    # Request to get values from the specified range in the Google Sheet
    result = (sheet.values().get(
        spreadsheetId=spreadsheet_id,
        range=f'{sheet_name}!{replace_range}',
    ).execute())

    # Extract the values from the response
    values = result.get('values', [])

    # If the spreadsheet is empty, log an info message and return None
    if not values:
        print('No data found.')
        return None

    # Log the values and return them
    print(values)
    return values


def replace_sheet_with_csv(
        spreadsheet_id: str,
        csv_file_path: str,
        sheet_name: str,
        replace_range: str,
        credentials_file_path: str = 'sheets_credentials.json'
):
    """
    Replaces the values of a spreadsheet with the contents of a CSV file
    :param spreadsheet_id: id of the spreadsheet
    :param csv_file_path: the path where the CSV is stored
    :param sheet_name: name of the sheet within the spreadsheet
    :param replace_range: range to replace (e.g. A1:D5)
    :param credentials_file_path: path to the Google Cloud credentials
    """
    # Read the CSV file
    with open(csv_file_path, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        values = list(reader)  # Convert the CSV reader to a list of lists

    # Authenticate and build the service
    credentials = service_account.Credentials.from_service_account_file(credentials_file_path, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    sheets = service.spreadsheets()

    # Clear the existing values in the specified range
    sheets.values().clear(
        spreadsheetId=spreadsheet_id,
        range=f'{sheet_name}!{replace_range}',
    ).execute()

    # Update the sheet with the new values from the CSV
    sheets.values().update(
        spreadsheetId=spreadsheet_id,
        range=f'{sheet_name}!{replace_range}',
        body={
            "values": values,
        },
        valueInputOption='USER_ENTERED'
    ).execute()


if __name__ == '__main__':
    sheet_id = os.environ.get('SPREADSHEET_ID')
    replace_sheet_with_csv(sheet_id, 'table_data.csv', 'vc', 'A1')
