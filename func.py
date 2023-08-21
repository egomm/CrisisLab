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

# Function for finding an available port
def find_port(start_port=1, max_port=256):
    import serial
    for port_number in range(start_port, max_port + 1):
        port_name = f"COM{port_number}"
        try:
            ser = serial.Serial(port_name, baudrate=115200, timeout=2.5,
                                parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS,
                                stopbits=serial.STOPBITS_ONE)
            ser.close()  # Close the port after opening to test availability
            # Return the valid port
            return port_name
        except serial.SerialException as e:
            print(e)
            continue
    return None