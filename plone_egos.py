#!/usr/bin/python
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage

def send_hashtag_report(hashtag, *email_to):
    pass

def get_tweets(hashtag):
    pass

def get_image(image_url):
    pass

def prepare_email(tweets):
    pass


def send_email(addresses, host, port, from_address, subject):
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject
    msgRoot['From'] = from_address
    msgRoot['To'] = ', '.join(addresses)

    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = MIMEText('PLAIN TEXT GOES HERE')
    msgAlternative.attach(msgText)

    msgText = MIMEText('<b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>Nifty!', 'html')
    msgAlternative.attach(msgText)

    # This example assumes the image is in the current directory
    fp = open('image1.jpg', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)
    session = smtplib.SMTP(host, port)
    session.starttls()
    session.login(from_address, "_passw0rd_")
    session.sendmail(from_address, addresses, msgRoot.as_string())
    session.quit()


send_email(["james.sutterfield@gmail.com"], "smtp.gmail.com", 587, "nbpyclasstest@gmail.com", "A collection of Emerald Sprint tweets")