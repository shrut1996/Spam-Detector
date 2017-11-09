import imaplib
mail = imaplib.IMAP4_SSL('imap.gmail.com')
f=open("/home/aronzx/keys","r")
lines=f.readlines()
lines = [x.strip() for x in lines] 
mail.login(lines[0], lines[1])
f.close()
mail.list()
# Out: list of "folders" aka labels in gmail.
mail.select("inbox") # connect to inbox.

	
result, data = mail.uid('search', None, "ALL") # search and return uids instead
latest_email_uid = data[0].split()[-1]
result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
raw_email = data[0][1]

import email
def get_first_text_block(self, email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif maintype == 'text':
        return email_message_instance.get_payload()
email_message = email.message_from_string(raw_email)
 
print email_message['Received']
 
print email.utils.parseaddr(email_message['From']) # for parsing "Yuji Tomita" <yuji@grovemade.com>

#print email_message.items() # print all headers
 
# note that if you want to get text content (body) and the email contains
# multiple payloads (plaintext/ html), you must parse each message separately.
# use something like the following: (taken from a stackoverflow post)

