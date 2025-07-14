import os
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def create_google_service(client_secret_file, api_service_name, api_version, output_path, scopes):
    """Creates a Google API service.

    :param client_secret_file: Path to the client secret JSON file from Google Cloud Console.
    :param api_service_name: The name of the Google API service.
    :param api_version: The version of the Google API service.
    :param output_path: Path to the output JSON file storing the credentials.
    :param scopes: A list of scopes for the API service.
    :return: A service that is connected to the specified Google API.
    """
    cred = None

    # Check if the output JSON file with credentials exists
    if os.path.exists(output_path):
        with open(output_path, 'rb') as token:
            cred = json.load(token)

    # If there are no (valid) credentials available, let the user log in
    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret_file, scopes)
            cred = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(output_path, 'w') as token:
                token.write(cred.to_json())

    try:
        # Build the service
        service = build(api_service_name, api_version, credentials=cred)
        print(f"{api_service_name} service created successfully")
        return service
    except Exception as e:
        print(f"Failed to create service: {e}")
        return None


create_google_service(
    client_secret_file='sheets_credentials.json', # your input filename
    api_service_name='sheets',
    api_version='v4',
    output_path='google-sheet-api-token.json', # your output filename
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
