import email

NOT_PARSED_EMAIL = email.message_from_string("""Delivered-To: www+ABC123@example.com
Received: by 2002:a67:2e8e:0:0:0:0:0 with SMTP id u136-v6csp415684vsu;
        Fri, 14 Sep 2018 02:07:56 -0700 (PDT)
    d=example.com;
    h=content-type:from:mime-version:reply-to:to:subject; s=s1;
    bh=7SbJ/tkM//1UlEfLtZ+14BZ/4mg=; b=mQR92jguhR+dyu2+N08eSnR8pdl0a
    qr3IhF+POtGKAg+uCzMH9Oo0lElPkJnBXspJtvI4iHSaSGk2LFeAwC8DeJBTNA3x
    cQE4O0tkxv1ey9Ag2jspXAIuwxidwTA2x+kBp2/1klDDcz7ox4GNtRhs1jzKvBfG
    0rYO13NQsJN8oI=
DKIM-Signature: v=1; a=rsa-sha1; c=relaxed/relaxed; d=sendgrid.info;
    h=content-type:from:mime-version:reply-to:to:subject:x-feedback-id;
    s=smtpapi; bh=7SbJ/tkM//1UlEfLtZ+14BZ/4mg=; b=qCGxpDc8EoncgDH/2B
    7SbPnVvlQE8Yeypx4+If0QXCiMpqfT+PIn8MLydBmWHEEb4Wk76ja/9rtCR82o/S
    ji/inR+AGk4wYCO+1qKUP85CJB8Ml6vFcnq3O8+ooHeKFJl3LhMHHdvfrkM0tZ8k
    1Cfmym9d6Xr4hdRTm5hZWzk/4=
Received: by filter0056p3mdw1.sendgrid.net with SMTP id filter0056p3mdw1-14058-5B9B7A69-15
        2018-09-14 09:07:53.501556299 +0000 UTC m=+204732.967143206
Received: from NjkxMzM5Mg (ec2-35-160-91-185.us-west-2.compute.amazonaws.com [35.160.91.185])
    by ismtpd0005p1las1.sendgrid.net (SG) with HTTP id fxWHgR1QTBis-rEZKrOIFA
    Fri, 14 Sep 2018 09:07:53.395 +0000 (UTC)
Content-Type: multipart/alternative; boundary=d31cee9360929dfd2b7189018fea70c9cb1f37d213ed5b0b935841455965
Date: Fri, 14 Sep 2018 09:07:53 +0000 (UTC)
From: "Support" <notification+ABC123@example.com>
Mime-Version: 1.0
Reply-to: support@example.com
To: test test <www+ABC123@example.com>
Message-ID: <fxWHgR1QTBis-rEZKrOIFA@ismtpd0005p1las1.sendgrid.net>
Subject: Reset your password
X-SG-EID: de8IIHdyL1it6Yew7Ep1KMVq0UaO1RjaS41G0NzLV3etAOcU7kl6JZAzg0l6vQ2Wnfw25FeasQYNPd
 BX0/4PkH5ChSvuoWpsC0S6REXNIeDDU0ShKtGDoJoPeSZ8tM9w9V6IFaLHxjQMqtGo57/UnjNaVaw5
 tEfdGwOaDdRlFZfgkFxeqsHVBDBaMGhOBmOufynQb+3UQ9k1RCaZ4DCBrlQRhGW68DMW3LnA7N9x2O
 BlvrP9en5qqxY85M9TkVj896H0U0EOUp9f3yiB0qefwA==
X-SG-ID: ej4nT81hSxGYlXaeVp3cI2yy1N8ZLMVhnwFf9jVfZExVnBvLl1x3CTTEaa/i0ip1+cbjxyfhNN29oP
 DXJpd1Fv0wGn6pAyl3YX3SqBfQ/A4+6CCQXlwoHTSsCHlycBVc
X-Feedback-ID: 6913392:h6VWkon+v2fnC9kyZ7xLDtz/0CAQPD/8O52AB4Yvi1E=:sucKYeTyQIs7YiTfKRWk7Is3wQ5gxvi/cOwDYnPm1cc=:SG
--d31cee9360929dfd2b7189018fea70c9cb1f37d213ed5b0b935841455965
content-transfer-encoding: quoted-printable
content-type: text/plain; charset="UTF-8"
Mime-Version: 1.0
Here's your password reset code.
Hi tset,
We have received a request to reset your password. To complete this =
request, please enter the code below into the password reset form.=C2=A0
Password Reset Code:=C2=A0
5F5X3B
Thank you,
The Amazing Team
If you have any questions, please contact us at support@myexample.com mai=
lto:support@myexample.com?subject=3DReply%20to%20Password%20Reset or by r=
eplying to this email.
--d31cee9360929dfd2b7189018fea70c9cb1f37d213ed5b0b935841455965
content-transfer-encoding: quoted-printable
content-type: text/html; charset="UTF-8"
Mime-Version: 1.0
--d31cee9360929dfd2b7189018fea70c9cb1f37d213ed5b0b935841455965--
""")
PARSED_EMAIL = """Here's your password reset code.
Hi tset,
We have received a request to reset your password. To complete this =
request, please enter the code below into the password reset form.=C2=A0
Password Reset Code:=C2=A0
5F5X3B
Thank you,
The Amazing Team
If you have any questions, please contact us at support@myexample.com mai=
lto:support@myexample.com?subject=3DReply%20to%20Password%20Reset or by r=
eplying to this email."""