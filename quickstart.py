from __future__ import print_function

import json
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
from get import GetMessage
from list import ListMessagesMatchingQuery
from main import detect_suspicous_content

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
f = open('output.txt', 'w+')


def main():

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    all_messages = ListMessagesMatchingQuery(service, "me", "label:inbox")
    from_name = ''
    return_path = ''
    subject = ''

    if not all_messages:
        print('No message')
    else:
        for message in all_messages:
            message_content = GetMessage(service, "me", message["id"])
            print('\n\nMessage content: %s' % message_content['snippet'])
            for header in message_content['payload']['headers']:
                # if header['name'] == 'From':
                #     print('From: %s' % header["value"])
                # if header['name'] == 'Return-Path':
                #     print('return path: %s' % header['value'])
                if header['name'] == 'From':
                    from_name = header['value'].split()[-1]
                if header['name'] == 'Return-Path':
                    print(header['value'].split())
                    return_path = header['value'].split()[-1]
                if header['name'] == 'Subject':
                    subject = header['value']
            if (detect_suspicous_content(subject.split()) or detect_suspicous_content(message_content['snippet'].split()) or from_name != return_path):
                f.write('From: ' + from_name + ' Return-Path: ' + return_path + ' Subject: ' + subject + ' Body: ' +
                        message_content['snippet'] + '\n')
                #f.write(json.dumps(message_content))

    f.close()


if __name__ == '__main__':
    main()