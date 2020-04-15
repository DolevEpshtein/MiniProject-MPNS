
from apiclient import errors

from apiclient import errors
import re


def GetAttachments(service, user_id, msg_id):
    """Get and store attachment from Message with given id.
        Args:
            service: Authorized Gmail API service instance.
            user_id: User's email address. The special value "me"
                can be used to indicate the authenticated user.
            msg_id: ID of Message containing attachment.
    """
    try:
        file_names = []
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()
        if 'parts' in message['payload']:
            for part in message['payload']['parts']:
                    extentions = re.findall("(?<=\.)([a-zA-Z]+?)(?=\.)", part['filename']) + re.findall("(?<=\.)([a-zA-Z]+?)(?=$)", part['filename'])
                    extenstions_set_without_duplication = set(extentions) - set(file_names)
                    file_names = file_names + list(extenstions_set_without_duplication)
        return file_names

        '''
        if part.get('filename'):
                if 'data' in part['body']:
                    file_data = base64.urlsafe_b64decode(part['body']['data'].encode('UTF-8'))
                    # print('FileData for %s, %s found! size: %s' % (message['id'], part['filename'], part['size']))
                elif 'attachmentId' in part['body']:
                    attachment = service.users().messages().attachments().get(
                        userId=user_id, messageId=message['id'], id=part['body']['attachmentId']
                    ).execute()
                    file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))
                    # print('FileData for %s, %s found! size: %s' % (message['id'], part['filename'], attachment['size']))
                else:
                    file_data = None
                if file_data:
                    return part.get('filename')
        '''


    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def get_message(service, user_id, msg_id):
    """
    Get a Message with given ID.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      msg_id: The ID of the Message required.

    Returns:
      A Message.
    """
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()

        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def get_list_of_messages_by_query(service, user_id, query=''):
    """List all Messages of the user's mailbox matching the query.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      query: String used to filter messages returned.
      Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

    Returns:
      List of Messages that match the criteria of the query. Note that the
      returned list contains Message IDs, you must use get with the
      appropriate ID to get the details of a Message.
    """
    try:
        response = service.users().messages().list(userId=user_id,
                                                   q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query,
                                                       pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except errors.HttpError as error:
        print('An error occurred: %s' % error)