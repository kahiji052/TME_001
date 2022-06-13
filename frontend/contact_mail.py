import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# environment variables
username = 'toymodel.engineering@gmail.com'
password = 'kxckvvsvnqznxnkx'


def send_mail(text = 'Email Body', subject = 'Soporte', from_email='Toy Model Engineering <toymodel.engineering.com>', to_emails = None, html = None):
    assert isinstance(to_emails, list)
    msg = MIMEMultipart('alternative')
    msg['From'] = from_email 
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject
    txt_part = MIMEText(text, 'plain')
    msg.attach(txt_part)
    html = "<h3>¡Hola! Hemos recibido tu solicitud de contacto.<h3><br><p>Si deseas añadir más comentarios, puedes hacerlo respondiendo este correo. Pronto alguien de nuestro equipo se pondrá en contacto contigo, ¡gracias!</p>"
    if html != None:
        html_part = MIMEText(html, 'html')
        msg.attach(html_part)
    msg_str = msg.as_string()
    # login to my smtp server
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(from_email, to_emails, msg_str)
    server.quit()