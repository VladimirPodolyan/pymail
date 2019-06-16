from datetime import datetime
from unittest import mock
import smtplib
import pytest
import random
import os

from src.mail_client import MailClient
from src.email_records import NOT_PARSED_EMAIL, PARSED_EMAIL


GET_TOKEN = os.environ['GMAIL_TOKEN']


def create_email(random_stamp: int):
    pid = os.getpid()
    rdm_digit = random.randint(0, 1000)
    timestamp_tag = datetime.now().isoformat('-', timespec='seconds').replace(':', '-')
    return f'pymail.auto+pid-{pid}-{random_stamp}-{rdm_digit}-sm-at-{timestamp_tag}@gmail.com'


@pytest.fixture
def smtp_client():
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login('pymail.auto@gmail.com', GET_TOKEN)
    return server


@pytest.fixture
def imap_client():
    return MailClient('pymail.auto@gmail.com', GET_TOKEN)


def send_mail(server, to, text, subject=None):
    available_subject = f'Subject: {subject}\n' if subject else '\n'
    to_address = f'Delivered-To: {to}\n'
    complete_body = f'{to_address}{available_subject}{text}'
    return server.sendmail('pymail.auto@gmail.com', to, complete_body)


def test_empty_label(imap_client):
    """ should be AssertionError if inbox is empty """
    try:
        imap_client._email_data_by_id(label='empty_label')
    except AssertionError:
        pass
    else:
        raise pytest.fail()


def test_get_email_from_last_few(imap_client, smtp_client):
    """ get_mail_text_from_last_few find expected email by 'Delivered-To' address """
    random_count_of_letters = random.randint(3, 9)
    addresses_array = []

    for count in range(random_count_of_letters):
        email_address = create_email(random_stamp=count)
        addresses_array.append(email_address)
        send_mail(smtp_client, email_address, text=PARSED_EMAIL, subject='Test pymail')

    expected_email_1 = random.choice(addresses_array)
    expected_email_2 = random.choice(addresses_array)
    assert (
        imap_client.get_mail_text_from_last_few(expected_email=expected_email_1, last_few=random_count_of_letters * 3),
        imap_client.get_mail_text_from_last_few(expected_email=expected_email_2, last_few=random_count_of_letters * 3)
    )


# Tests with mocked data


@pytest.fixture()
def mocked_imap_client():
    MailClient.__init__ = mock.MagicMock(return_value=None)
    MailClient._email_data_by_id = mock.MagicMock(return_value=NOT_PARSED_EMAIL)
    MailClient._email_data_from_last_few = mock.MagicMock(return_value=NOT_PARSED_EMAIL)
    return MailClient()


def test_delivered_to(mocked_imap_client):
    """ delivered_to is searching and return valid email address """
    to_address = mocked_imap_client.delivered_to(NOT_PARSED_EMAIL)
    assert to_address == 'www+ABC123@example.com'


def test_get_first_text_block(mocked_imap_client):
    """ get_first_text_block is parsing raw email text and should equal parsed email text """
    email_message = mocked_imap_client.get_first_text_block(NOT_PARSED_EMAIL)
    assert email_message == PARSED_EMAIL


def test_get_label_mail_text_by_sequence(mocked_imap_client):
    """ get_mail_text_by_id return parsed email text """
    email_message = mocked_imap_client.get_mail_text_by_id()
    assert email_message == PARSED_EMAIL


def test_get_expected_email_text(mocked_imap_client):
    """ email with 'Delivered-To' found and it should equal parsed email text """
    email_message = mocked_imap_client.get_mail_text_from_last_few('www+ABC123@example.com')
    assert email_message == PARSED_EMAIL


def test_get_expected_email_text_negative(mocked_imap_client):
    """ negative test - email with 'Delivered-To' not found """
    try:
        mocked_imap_client.get_mail_text_from_last_few('my.email@example.com', timeout=2)
    except AssertionError:
        pass
    else:
        raise pytest.fail()
