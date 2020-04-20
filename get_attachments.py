import win32com.client
import os

path = os.path.expanduser("~\Desktop\Attachments")
senders = ['Matthew Kingsley',
           'Darren Pope']

outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6)
messages = inbox.Items

for message in messages:
    for attachment in message.Attachments:
        if message.SenderName in senders and message.Unread:
            attachment.SaveAsFile(os.path.join(path, str(attachment)))
