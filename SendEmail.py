
def send_email(recipients, height):
    import smtplib

    smtp = smtplib.SMTP("smtp.office365.com", port=587)
    smtp.starttls()
    smtp.login('crisislabbot@outlook.com', 'CrisisLab')

    FROM = "crisislabbot@outlook.com"
    TO = recipients

    SUBJECT = "CrisisLab Warning!"
    TEXT = "CrisisLab has detected a possible tsunami with a height of %dm. Please be prepared." % height

    message = """From: %s\r\nTo: %s\r\nSubject: %s\r\n\

    %s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    smtp.sendmail(FROM, TO, message)
    smtp.quit()