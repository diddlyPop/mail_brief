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
    matchUPS1 = r"/\b(1Z ?[0-9A-Z]{3} ?[0-9A-Z]{3} ?[0-9A-Z]{2} ?[0-9A-Z]{4} ?[0-9A-Z]{3} ?[0-9A-Z]|[\dT]\d\d\d ?\d\d\d\d ?\d\d\d)\b/"
    matchUPS2 = r"/^[kKJj]{1}[0-9]{10}$/"
    matchUSPS0 = r"/(\b\d{30}\b)|(\b91\d+\b)|(\b\d{20}\b)/"
    matchUSPS1 = r"/(\b\d{30}\b)|(\b91\d+\b)|(\b\d{20}\b)|(\b\d{26}\b)| ^E\D{1}\d{9}\D{2}$|^9\d{15,21}$| ^91[0-9]+$| ^[A-Za-z]{2}[0-9]+US$/i"
    matchUSPS2 = r"/^E\D{1}\d{9}\D{2}$|^9\d{15,21}$/"
    matchUSPS3 = r"/^91[0-9]+$/"
    matchUSPS4 = r"/^[A-Za-z]{2}[0-9]+US$/"
    matchUSPS5 = r"/(\b\d{30}\b)|(\b91\d+\b)|(\b\d{20}\b)|(\b\d{26}\b)| ^E\D{1}\d{9}\D{2}$|^9\d{15,21}$| ^91[0-9]+$| ^[A-Za-z]{2}[0-9]+US$/i"
    matchFedex1 = r"/(\b96\d{20}\b)|(\b\d{15}\b)|(\b\d{12}\b)/"
    matchFedex2 = r"/\b((98\d\d\d\d\d?\d\d\d\d|98\d\d) ?\d\d\d\d ?\d\d\d\d( ?\d\d\d)?)\b/"
    matchFedex3 = r"/^[0-9]{15}$/"
    patterns = [matchFedex1, matchFedex2, matchFedex3, matchUSPS0, matchUSPS1, matchUSPS2, matchUSPS3, matchUSPS4, matchUSPS5, matchUPS1, matchUPS2]

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
            for pattern in patterns:
                match = re.search(pattern, email)
                if match and match.group() not in match_emails:
                    match_emails.append(match.group())

        print("number of matching emails with tracking # patterns: %d" % len(match_emails))
        if len(match_emails) > 0:
            for match in match_emails:
                print("Tracking number found: " + match)



