import email
import imaplib
import time
import timeit
import logging
from inspect import currentframe
from os.path import basename


def log(message):
    """ Log in format [level][module][function:line] """
    func = currentframe().f_back.f_code
    logging.log(logging.ERROR, f'[{basename(func.co_filename)}][{func.co_name}:{func.co_firstlineno}] {message}')


class MailClient(object):
    """
        Basic reusable mail client for boxes on gmail.com hosting
        You must allow in account setting "login from less secure devices" first!
    """
    def __init__(self, email_address, password, label='inbox', auto_login=True):
        """
            Initiate email client, login with given credentials and select label (by default - 'inbox')
            :param email_address: email address for login
            :param password: password for email address for login
            :param label: target label
        """
        self.email_address = email_address
        self.password = password
        self.label = label
        self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
        if auto_login:
            self.login_and_select_label()

    def login_and_select_label(self):
        self.mail.login(self.email_address, self.password)
        self.mail.select(self.label)

    def logout(self):
        self.mail.close()
        self.mail.logout()

    def get_mail_text_by_id(self, label=None, flag='ALL', index=-1):
        """
            Get required mail text by index
            :param flag: additional filter for gmail messages ~ flag='Subject "Welcome to Gmail!"'
                all flags variables - https://gist.github.com/martinrusev/6121028;
            :param index: index of required mail (bigger is newer) ~ index=-1
            :param label: target label. Will be used this label if then different from MailClient ~ label='inbox'
            :return: parsed text of mail from last mail
        """
        text_block = self._get_first_text_block(self._email_data_by_id(label, flag, index))
        return text_block

    def get_mail_text_from_last_few(self, expected_email, flag='ALL', last_few=3, timeout=30, label=None):
        """
            Get required mail text, until "To" address is equal to the "Expected" address
            Standard time for request - one time in the one second (with a lot of data)
            You can set last_few = 1, and then the search will be performed on the last email
            :param expected_email: expected email address who received the message
            :param flag: additional filter for gmail messages ~ flag='Subject "Welcome to Gmail!"'
              all flags variables - https://gist.github.com/martinrusev/6121028;
            :param timeout: time to exit the loop (end fetching data) ~ index=-1
            :param last_few: number of recent emails among which will be searched by expected_email ~ 5
            :param label: target label. Will be used this label if then different from MailClient ~ label='inbox'
            :return: parsed text of mail for expected address from last few letters
        """
        message_instance = self._email_data_from_last_few(expected_email=expected_email, label=label,
                                                          flag=flag, last_few=last_few)
        actual_email = self._delivered_to(message_instance)
        loop_start = timeit.default_timer()
        get_timeout = 0

        while expected_email != actual_email and get_timeout <= timeout:
            message_instance = self._email_data_from_last_few(expected_email=expected_email,
                                                              flag=flag, last_few=last_few, label=label)
            get_timeout = int(timeit.default_timer() - loop_start)
            actual_email = self._delivered_to(message_instance)

        assert expected_email == actual_email, f'Message for {expected_email} with current settings not found'
        return self._get_first_text_block(message_instance)

    def _delivered_to(self, email_message_instance):
        """
            Address FOR which the email is delivered
            :param email_message_instance: content of mail if it's available to parse
            :return: email address for which the email is delivered
        """
        if email_message_instance is None:
            address = None
        else:
            address = email_message_instance['Delivered-To']
        return address

    def _email_data_by_id(self, label=None, flag='ALL', index=-1):
        """
            Get required mail from label of mailbox by index (bigger is newer)
            :param flag: additional filter for gmail messages ~ flag='Subject "Welcome to Gmail!"'
                all flags variables - https://gist.github.com/martinrusev/6121028;
            :param index: index of required mail (bigger is newer) ~ index=-1
            :param label: target label. Will be used this label if then different from MailClient ~ label='inbox'
            :return: content of mail if it's available to parse
        """
        self._change_label(label)

        try:
            self._id_list(flag)[index]
        except IndexError:
            log(f'Index={index} isn\'t valid for label={self.label} with flag={flag}. Used default index=-1.')
            index = -1

        result, data = self.mail.fetch(self._id_list(flag)[index], '(RFC822)')
        item = len(data) - 2
        raw_email = data[item][1].decode('utf-8')
        return email.message_from_string(raw_email)

    def _email_data_from_last_few(self, expected_email, flag='ALL', last_few=3, label=None):
        """
            Get required mail from label of mailbox from last few mails

            :param expected_email: expected email address who received the message;
            :param flag: additional filter for gmail messages. Example ~ 'Subject "Welcome to Gmail!"'
              all flags variables - https://gist.github.com/martinrusev/6121028;
            :param last_few: number of recent emails among which will be searched;
            :param label: target label. Will be used this label if then different from MailClient;
            :return: None if mail for address not found, else content of mail if it's available to parse
        """
        self._change_label(label)

        expected_email_message_instance = None

        for num in self._id_list(flag)[-last_few:]:
            result, data = self.mail.fetch(num, '(RFC822)')
            item = len(data) - 2
            raw_email = data[item][1].decode('utf-8')
            message_instance = email.message_from_string(raw_email)
            actual_email = self._delivered_to(message_instance)
            if expected_email == actual_email:
                expected_email_message_instance = message_instance
                return expected_email_message_instance

        return expected_email_message_instance

    def _id_list(self, flag='ALL'):
        """
            Get id list of required emails. Also fetch data in 10 seconds if inbox is empty
            :param flag: additional filter for gmail messages. Example ~ 'Subject "Welcome to Gmail!"'
              all flags variables - https://gist.github.com/martinrusev/6121028;
            :return: emails id as [b'1 2 3 4']
        """

        def update_data():
            self.mail.noop()
            status, actual_data = self.mail.search(None, f'({flag})')
            assert status == 'OK', 'Can not validate result code of mail listing!'
            return actual_data

        loop_start = timeit.default_timer()
        get_timeout = 0
        data = update_data()

        while not data[0].split() and get_timeout <= 10:
            get_timeout = int(timeit.default_timer() - loop_start)
            time.sleep(0.1)
            data = update_data()

        assert data[0].split(), f'List of email messages in "{self.label}" with flag={flag} is empty!'
        id_list = data[0].split()
        return id_list

    def _get_first_text_block(self, email_message_instance):
        """
            Parse the mail content to the text
            :param email_message_instance: content of mail if it's available to parse
            :return: parsed text of mail content
        """
        maintype = email_message_instance.get_content_maintype()
        if maintype == 'multipart':
            for part in email_message_instance.get_payload():
                if part.get_content_maintype() == 'text':
                    return part.get_payload()
        elif maintype == 'text':
            return email_message_instance.get_payload(decode=True)

    def _change_label(self, label):
        new_label = self.label if not label else label
        if new_label != self.label:
            self.mail.select(new_label)
