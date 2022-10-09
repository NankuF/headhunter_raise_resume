import email
import logging
import sys
import time
from email.header import decode_header

import emails.functions as functions


logger = logging.getLogger('app.read_email')

def get_auth_code():
    imap = functions.connection()
    if not imap:
        sys.exit()

    status, messages = imap.select("hh_codes")  # папка hh_codes
    code = None
    while True:
        res, unseen_msg = imap.uid("search", "UNSEEN", "ALL")
        unseen_msg = unseen_msg[0].decode("utf-8").split(" ")

        if unseen_msg[0]:
            for letter in unseen_msg:
                attachments = []
                res, msg = imap.uid("fetch", letter, "(RFC822)")
                if res == "OK":
                    msg = email.message_from_bytes(msg[0][1])

                    msg_date = functions.date_parse(email.utils.parsedate_tz(msg["Date"]))
                    msg_from = functions.from_subj_decode(msg["From"])
                    msg_subj = functions.from_subj_decode(msg["Subject"])
                    msg_id = msg["Message-ID"].lstrip("<").rstrip(">")
                    msg_email = msg["Return-path"].lstrip("<").rstrip(">")
                    if not msg_email:
                        msg_email = (
                            decode_header(msg["From"])[1][0]
                            .decode()
                            .replace("<", "")
                            .replace(">", "")
                            .replace(" ", "")
                        )

                    letter_text = functions.get_letter_text(msg)
                    attachments = functions.get_attachments(msg)
                    if msg_subj == 'Код подтверждения':
                        return letter_text.replace(' ', '').replace('\n', '').replace('\r', '').replace('=', '')[:4]
        else:
            logger.info('На email еще не пришел код авторизации.')
            time.sleep(120)


if __name__ == '__main__':
    get_auth_code()
