import datetime
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define the scopes required for accessing the Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'C:/Users/Atharva/OneDrive/Desktop/Codeshastra/CodeShastra_Ctrl-Alt-Elite_SmitShah/Credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def create_event(summary, location, start_time, end_time):
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    event = {
      'summary': summary,
      'location': location,
      'start': {
        'dateTime': start_time.strftime('%Y-%m-%dT%H:%M:%S'),
        'timeZone': 'Asia/Kolkata',  # Example: 'America/Los_Angeles'
      },
      'end': {
        'dateTime': end_time.strftime('%Y-%m-%dT%H:%M:%S'),
        'timeZone': 'Asia/Kolkata',  # Example: 'America/Los_Angeles'
      }
    }

    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))
    except HttpError as e:
        print('Error creating event:', e)

if __name__ == '__main__':
    # Example usage
    summary = 'Meeting with client'
    location = 'Office'
    start_time = datetime.datetime(2024, 4, 1, 10, 0)  # Example: April 1, 2024 at 10:00 AM
    end_time = datetime.datetime(2024, 4, 1, 11, 0)    # Example: April 1, 2024 at 11:00 AM
    create_event(summary, location, start_time, end_time)
