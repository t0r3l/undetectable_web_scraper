#documentation https://thepythoncode.com/article/use-gmail-api-in-python
from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
# for dealing with attachement MIME types
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from io import BytesIO



##################################################################

def connect2gmail():
    #choose SCOPE https://developers.google.com/gmail/api/auth/scopes
    SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify',
]
    credentials_path =  "C:/Users/morel/Documents/Library/CodingTime/GitHub/robinhood/Scrap/gmai1/log_files/client_secret.json"
    token_path =   "C:/Users/morel/Documents/Library/CodingTime/GitHub/robinhood/Scrap/gmai1/log_files/token.json"
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        return service

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')

   
####################################

def search_messages(service, query):
    result = service.users().messages().list(userId='me',q=query).execute()
    messages = [ ]
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages

######################################
    
def parse_parts(service, parts):
    """
    Utility function that parses the content of an email partition
    """
    if parts:
        for part in parts:
            mimeType = part.get("mimeType")
            body = part.get("body")
            data = body.get("data")
            part_headers = part.get("headers")
            if part.get("parts"):
                # recursively call this function when we see that a part
                # has parts inside
                parse_parts(service, part.get("parts"))
            if mimeType == "text/plain":
                # if the email part is text plain
                if data:
                    data = str(urlsafe_b64decode(data).decode())
            return data


#############################

def read_command(service, message):
    """
    This function takes Gmail API `service` and the given `message_id` and does the following:
        - Downloads the content of the email
        - Prints email basic information (To, From, Subject & Date) and plain/text parts
        - Creates a folder for each email based on the subject
        - Downloads text/html content (if available) and saves it under the folder created as index.html
        - Downloads any file that is attached to the email and saves it in the folder created
    """
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    # parts can be the message body, or attachments
    payload = msg['payload']
    headers = payload.get("headers")
    parts = payload.get("parts")
    body2return = parse_parts(service, parts)
    #mark as read
    service.users().messages().batchModify(
      userId='me',
      body={
          'ids': msg['id'],
          'removeLabelIds': ['UNREAD']
      }
    ).execute()
    return body2return
###############################################

def read_last_command(service, query):
    # get emails that match the query you specify
    results = search_messages(service, query)
    if len(results) != 0:
        #takes the last unread message as command and mark others as read
        i = 0
        for message in results:
            if i == 0:
                #messages are read in ascending order, so newest one is read first
                command = read_command(service, message)
            else:
                mark_as_read(message)
            i += 1
    else:
        command = 'no passa nada'
    return command


###################################################

def mark_as_read(service, message):
    service.users().messages().batchModify(
      userId='me',
      body={
          'ids': message['id'],
          'removeLabelIds': ['UNREAD']
      }
    ).execute()



###########################################################################


def send_message(service, destination, obj, text, workbook=None):
    programMailBox = 'your_email@gmail.com'

    if workbook is None:
        # Build text message
        message = MIMEText(text)
    else:
        # Create a BytesIO object to store the Excel workbook
        xlsx_data = BytesIO()

        # Save the workbook to the BytesIO object as XLSX
        workbook.save(xlsx_data)
        xlsx_data.seek(0)

        # Build a multipart message
        message = MIMEMultipart()

        # Attach the XLSX file to the email
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(xlsx_data.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename=your_file.xlsx")
        message.attach(part)

    # Send the message
    message['to'] = destination
    message['from'] = programMailBox
    message['subject'] = obj
    toSend = {'raw': urlsafe_b64encode(message.as_bytes()).decode()}
    service.users().messages().send(
        userId="me",
        body=toSend
    ).execute()