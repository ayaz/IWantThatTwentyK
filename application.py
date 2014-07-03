#!/usr/bin/env python

from flask import Flask
import requests
import local_settings

app = Flask(__name__)

@app.route("/")
def IsItTwentyKYet():
    url = "https://api.digitalocean.com/droplet_count"
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36"
    headers = {'User-Agent': user_agent}

    try:
        req = requests.get(url, headers=headers)
    except Exception, e:
        send_mail("Exception: %s" % e, "%s" % e)
    try:
        count = int(req.text)
    except Exception, e:
        send_mail("Exception: %s" %e, "%s %s" % (count, e))
    else:
        if count >= 1999900 and count <= 1999980:
            send_mail("Reched 1999900!", "Reached 1999900!")
        elif count > 1999980 and count <= 1999990:
            send_mail("ALERT: reached 1999990!", "ALERT: reached 1999990!")
        elif count >= 1999995:
            send_mail("HIGH ALERT: reached 1999995", "HIGH ALERT: reached 1999995")
    return "OK"



def send_mail(subject, message):
    import smtplib
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText

    gmailUser = local_settings.gmail_user
    gmailPassword = local_settings.gmail_password
    recipient = local_settings.recipient

    msg = MIMEMultipart()
    msg['From'] = gmailUser
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(message))

    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmailUser, gmailPassword)
    mailServer.sendmail(gmailUser, recipient, msg.as_string())
    mailServer.close()



if __name__ == "__main__":
    app.run(host='127.0.0.1')
