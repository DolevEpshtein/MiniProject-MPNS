from __future__ import print_function

import pickle
import os.path
import re
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from mail_reader import get_message
from mail_reader import get_list_of_messages_by_query
from suspicious_words_detector import detect_suspicious_content

# If modifying these scopes, delete the file token.pickle

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

    # the instance object accessing the email account
    service = build('gmail', 'v1', credentials=creds)
    all_messages = get_list_of_messages_by_query(service, "me", "label:inbox")
    from_name = ''
    return_path = ''
    reply_to = ''
    subject = ''
    date = ''
    suspected_counter = 0
    total_counter = 0

    if not all_messages:
        print('No message')
    else:
        str_total_result = ''
        for message in all_messages:
            message_content = get_message(service, "me", message["id"])
            for header in message_content['payload']['headers']:

                if header['name'] == 'From':
                    # use regex to extract email address
                    from_name = re.search("(?<=<)[\s\S]+(?=>)", header['value'])[0]
                if header['name'] == 'Return-Path':
                    return_path = header['value'].split()[-1]
                if header['name'] == 'Reply-To':
                    reply_to = header['value'].split()[-1]
                if header['name'] == 'Subject':
                    subject = header['value']
                if header['name'] == 'Date':
                    date = header['value']
            suspicious_content_result = detect_suspicious_content(subject.split()) + \
                                        detect_suspicious_content(message_content['snippet'].split())
            str_result = ''
            if len(suspicious_content_result) > 0:
                str_result = str_result + '\nThis email contains suspicious words, you may be a victim of a fishing attack' + str(
                    suspicious_content_result)
            if from_name != reply_to:
                str_result = str_result + '\nThis message is suspicious of being a spoofing email'
            if str_result != '':
                suspected_counter = suspected_counter + 1
                str_total_result = str_total_result + "\n\n" + "*" * 90 + str_result + '\n\nFrom: ' + from_name + '\nReply-To: ' + reply_to + '\nSubject: ' + subject + '\nBody: ' + \
                                   message_content['snippet'] + '\nDate: ' + date + '\n'
        total_counter = total_counter + 1
        f.write("\n\n\n" + " " * 70 + "*" * 25 + "\n" + " " * 70 + "*  Email Security Test  *\n" + " " * 70 + "*" * 25)
        f.write("\n\nScanning " + str(total_counter) + " messages...")
        if suspected_counter == 0:
            f.write("\n\nDidn't find any suspicious mails. Your account is secure")
        else:
            f.write("\n\nFound " + str(suspected_counter) + " suspicious messages")
            f.write(str_total_result)
    f.close()


if __name__ == '__main__':
    main()
