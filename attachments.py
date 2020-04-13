import base64
from apiclient import errors

def GetAttachments(service, user_id, msg_id, store_dir=""):
    """Get and store attachment from Message with given id.
        Args:
            service: Authorized Gmail API service instance.
            user_id: User's email address. The special value "me"
                can be used to indicate the authenticated user.
            msg_id: ID of Message containing attachment.
            store_dir: The directory used to store attachments.
    """
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()
        parts = [message['payload']]
        while parts:
            part = parts.pop()
            if part.get('parts'):
                parts.extend(part['parts'])
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

    except errors.HttpError as error:
        print('An error occurred: %s' % error)