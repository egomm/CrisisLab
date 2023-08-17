import smtplib

smtp = smtplib.SMTP("smtp.office365.com", port=587)
smtp.starttls()
smtp.login('crisislabbot@outlook.com', 'CrisisLab')

FROM = "crisislabbot@outlook.com"
TO = ["egomyt@gmail.com", "20130@wc.school.nz"] # must be a list

SUBJECT = "Test Email"
TEXT = "CrisisLab gives you a warning!"

# Prepare actual message
message = """From: %s\r\nTo: %s\r\nSubject: %s\r\n\

%s
""" % (FROM, ", ".join(TO), SUBJECT, TEXT)

smtp.sendmail(FROM, TO, message)
smtp.quit()