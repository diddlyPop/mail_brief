import email, pyzmail
from imapclient import IMAPClient

# mail.py uses credentials from credentials.txt to connect to an imap email.
# mail.py displays your most recent email
# mail.py uses IMAPclient and pyzmail modules

def start_connection():

    imap_url = 'imap.gmail.com'     # only works with gmail at this time

    def get_body(msg):
        if msg.is_multipart():
            return get_body(msg.get_payload(0))
        else:
            return msg.get_payload(None, True)

    def search(key, value, con):
        result, data = con.search(None, key, '"{}"'.format(value))
        return data

    with open('credentials.txt', 'r') as file:
        user = file.readline()
        password = file.readline()
        server = IMAPClient(imap_url, use_uid=True)
        server.login(user, password)
        select_info = server.select_folder('INBOX')
        print('%d messages in INBOX' % select_info[b'EXISTS'])
        messages = server.search(['FROM', 'events@pokerstars.com'])
        print("%d messages from google" % len(messages))
