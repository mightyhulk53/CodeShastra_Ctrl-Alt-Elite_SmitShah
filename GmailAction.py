from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

CLIENT_SECRET_FILE = 'C:/Users/Atharva/OneDrive/Desktop/Codeshastra/CodeShastra_Ctrl-Alt-Elite_SmitShah/GmailCredentials.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

emailMsg = 'You won $100,000'
mimeMessage = MIMEMultipart()
mimeMessage['to'] = 'smitshahofficial@gmail.com'
mimeMessage['subject'] = 'You won'
mimeMessage.attach(MIMEText(emailMsg, 'plain'))
raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
print(message)

def get_last_5_messages():
    try:
        response = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=5).execute()
        messages = response.get('messages', [])

        if not messages:
            print('No messages found.')
        else:
            print('Last 5 messages in the inbox:')
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                print('Message snippet: {}'.format(msg['snippet']))
    except Exception as e:
        print('An error occurred:', e)

if __name__ == '__main__':
    get_last_5_messages()