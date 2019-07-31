import imaplib, email


def start_connection():

    imap_url = 'imap.gmail.com'

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
        print('x'+user+'x')
        print('x'+password+'x')
        con = imaplib.IMAP4_SSL(imap_url)
        con.login(user, password)
        con.select('INBOX')

        result, data = con.fetch(b'11', '(RFC822)')

        raw = email.message_from_bytes(data[0][1])

        print(get_body(raw))
