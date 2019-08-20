import email, pyzmail
from imapclient import IMAPClient
import pyzmail
import sys
import re

# mail.py uses credentials from credentials.txt to attempt connection to an imap gmail email
# mail.py asks for a search term
# mail.py uses IMAPclient and pyzmail modules to search your gmail inbox against our search term
# mail.py may throw exceptions if it cannot pull the text_part from a message
# mail.py checks valid text_parts against our tracking number patterns
# mail.py contains a list (match_emails) that holds emails with a valid tracking number in the body

def start_connection():

    emails = []
    match_emails = []
    pattern1 = re.compile("/\b(1Z ?[0-9A-Z]{3} ?[0-9A-Z]{3} ?[0-9A-Z]{2} ?[0-9A-Z]{4} ?[0-9A-Z]{3} ?[0-9A-Z]|[\dT]\d\d\d ?\d\d\d\d ?\d\d\d)\b/")
    pattern2 = re.compile("/(\b96\d{20}\b)|(\b\d{15}\b)|(\b\d{12}\b)/")
    pattern3 = re.compile("/\b((98\d\d\d\d\d?\d\d\d\d|98\d\d) ?\d\d\d\d ?\d\d\d\d( ?\d\d\d)?)\b/")
    pattern4 = re.compile("/^[0-9]{15}$/")
    pattern5 = re.compile("/(\b\d{30}\b)|(\b91\d+\b)|(\b\d{20}\b)/")
    pattern6 = re.compile("/^E\D{1}\d{9}\D{2}$|^9\d{15,21}$/")
    pattern7 = re.compile("/^91[0-9]+$/")
    pattern8 = re.compile("/^[A-Za-z]{2}[0-9]+US$/")
    patterns = [pattern1, pattern2, pattern3, pattern4, pattern5, pattern6, pattern7, pattern8]

    imap_url = 'imap.gmail.com'     # only works with gmail at this time

    with open('credentials.txt', 'r') as file:
        user = file.readline()
        password = file.readline()

        server = IMAPClient(imap_url, use_uid=True)
        try:
            server.login(user, password)
        except:
            print("error with account details")
            sys.exit()
        select_info = server.select_folder('INBOX')
        print('%d messages in INBOX' % select_info[b'EXISTS'])
        search_query = input("search for: ")
        uids = server.gmail_search(search_query)
        print("%d matches found in gmail " % len(uids))
        messages = server.fetch(uids, ['BODY[]'])
        for x in messages.keys():
            message = pyzmail.PyzMessage.factory(messages[x][b'BODY[]'])
            try:
                emails.append(message.text_part.get_payload().decode(message.text_part.charset))
            except:
                print("error in this message: %d" % x)
        server.logout()
        print("putting regex against %d emails" % len(emails))
        for email in emails:
            if len(emails) < 25:
                print(email)
            for pattern in patterns:
                match = re.search(pattern, email)
                if match:
                    match_emails.append(email)
        print("number of matching emails with tracking # patterns: %d" % len(match_emails))

