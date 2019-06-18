# py-mail


The project will provide the ability to receive data from the gmail mailbox in human readable type.
For these purposes, there are two main functions:
1. `get_mail_text_from_last_few`
2. `get_mail_text_by_id`

### 1. get_mail_text_from_last_few
This function looks at each letter in the mailbox and return the letter for the specified user.
"How is this possible?" - `get_mail_text_from_last_few` requires a unique email address. For example:
 - `some.address+9014@gmail.com`
 - `some.address+currnet_date()@gmail.com`
 - `some.address+datetime.now()@gmail.com`
 
Arguments:
- `expected_email`: expected email address who received the message ~ `some.address+9014@gmail.com`
- `flag`: additional filter for gmail messages ~ `flag='Subject "Welcome to Gmail!"'`
- `timeout`: time to exit the loop in sec. (end fetching data) ~ `timeout=60`
- `last_few`: number of recent emails among which will be searched by expected_email ~ `last_few=5`
- `label`: target label. Will be used this label if then different from MailClient ~ `label='inbox'`

```python
from datetime import datetime

import pytest
from py_mail import MailClient

@pytest.fixture
def mail_client():
    mail_client = MailClient(email_address='some.address@gmail.com', password='AmazingPass', label='inbox')
    yield mail_client
    mail_client.logout()


def get_email_by_idimap_client(mail_client):
    expected_email = f'some.address+{datetime.now()}@gmail.com'
    mail = mail_client.get_mail_text_from_last_few(expected_email=expected_email, last_few=10, timeout=60)
    return mail  # or you can search some specific data from letter via regex
```


### 2. get_mail_text_by_id
This function takes the letter by index (the last one is by default) and returns its content (text).
The downside is that you can get the wrong email:
because of problems with long delivery or because of the large number of incoming letters

Arguments:
- `label` - additional filter for gmail messages ~ `flag='Subject "Welcome to Gmail!"'`
- `flag` - target label. Will be used this label if then different from MailClient ~ `label='inbox'`
- `index` - index of required mail (bigger is newer) ~ `index=-1`

```python
import pytest
from py_mail import MailClient

@pytest.fixture
def mail_client():
    mail_client = MailClient(email_address='some.address@gmail.com', password='AmazingPass', label='inbox')
    yield mail_client
    mail_client.logout()


def get_email_by_id(mail_client):
    mail = mail_client.get_mail_text_by_id(label='other inbox', flag='subject "Confirm your device"')
    return mail  # or you can search some specific data from letter via regex
```


Useful Links:
- [regex](https://docs.python.org/3/library/re.html)
- [all flags variables](https://gist.github.com/martinrusev/6121028)