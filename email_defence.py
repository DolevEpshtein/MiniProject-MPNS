#!/usr/bin/env python3

from __future__ import print_function

import pickle
import os.path
import os
import re
import string
import shlex
import platform

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from mail_reader import GetAttachments
from mail_reader import get_message
from mail_reader import get_list_of_messages_by_query
from suspicious_words_detector import detect_suspicious_content

# If modifying these scopes, delete the file token.pickle
whitelisting_spoofed_mails = [".bounces.google.com"]
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
f = open('output.txt', 'w+', encoding="utf-8")


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
    from_name = return_path = subject = date = str_total_result = reply_to = ''
    suspected_counter = total_counter = 0

    if not all_messages:
        print('No message')
    else:
        for message in all_messages:
            message_content = get_message(service, "me", message["id"])

            attachments_extension_list = GetAttachments(service, "me", message["id"])

            for header in message_content['payload']['headers']:
                if header['name'] == 'From':
                    # use regex to extract email address
                    from_name = re.search("(?<=<)[\s\S]+(?=>)", header['value'])[0]
                if header['name'] == 'Return-Path':
                    return_path = re.search("(?<=<)[\s\S]+(?=>)", header['value'])[0]
                if header['name'] == 'Subject':
                    subject = header['value']
                if header['name'] == 'Date':
                    date = header['value']

            # clean up text
            subject_to_process = clean_noise(subject)
            content_tp_process = clean_noise(message_content['snippet'])


            suspicious_content_result = detect_suspicious_content(subject_to_process) + \
                detect_suspicious_content(content_tp_process)
            suspicious_extension_result = detect_suspicious_content(attachments_extension_list)

            str_result = ''
            if len(suspicious_content_result) > 0:
                str_result = str_result + '\nThis message contains suspicious words, it may be spam or a phishing attack: ' + ", ".join(suspicious_content_result)
            if len (suspicious_extension_result) > 0:
                str_result = str_result + '\nThis message contains suspicious files. It is risky to download and open files with the following extensions: ' + ", ".join(suspicious_extension_result)

            if from_name != return_path and not check_whitelist(return_path):
                str_result = str_result + '\nThis message is suspicious of being a spoofed email'

            if str_result != '':
                suspected_counter = suspected_counter + 1
                str_total_result = str_total_result + "\n\n" + "*" * 150 + str_result + '\n\nFrom: ' + from_name + '\nReturn-Path: ' + return_path + '\nSubject: ' + subject + '\nBody: ' + \
                                   message_content['snippet'] + '\nDate: ' + date + '\n'
            total_counter = total_counter + 1
        f.write("\n\n\n" + " " * 95 + "*" * 25 + "\n" + " " * 95 + "*  Email Security Test  *\n" + " " * 95 + "*" * 25)
        f.write("\n\nScanning " + str(total_counter) + " messages...")
        if suspected_counter == 0:
            f.write("\n\nDidn't find any suspicious mails. Your account is secure")
        else:
            f.write("\n\nFound " + str(suspected_counter) + " suspicious messages")
            f.write(str_total_result)
    f.close()
    start_file("output.txt", platform.system())

'''
    open the output file automatically based on the running os
'''

def start_file(filename, platform_type):
    if platform_type == 'Windows':
        os.system("start " + "output.txt")
    elif platform_type == 'Linux':
        os.system('gedit %s&' % filename)
    else:
        os.system("open " + shlex.quote("output.txt"))


'''
    convert all words to lower case, clean punctuation and ignore white spaces
'''
def clean_noise(text):
    words = text.split()
    table = str.maketrans('', '', string.punctuation)
    words = [w.translate(table) for w in words]
    words = [word.lower() for word in words]
    return ' '.join(words)


def check_whitelist(return_path):
    for white_address in whitelisting_spoofed_mails:
        if white_address in return_path:
            return True
    return False


main()
x = input("press enter to finish the program")