# mail_brief
mail_brief scans your emails for tracking numbers and notifies you of packages

requires python3, gmail email (must turn on "allow less secure apps")


currently:
- searches gmail inbox for a search term
- takes these emails and compares them against tracking number regex patterns
- takes all matches and puts them in a match_emails list

hope to add:
- twilio support
- imap support other than gmail

run gui.py
