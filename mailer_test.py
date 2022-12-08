import smtplib, ssl
from cowin_api import CoWinAPI
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
cowin = CoWinAPI()

port = 465 
stmp_host = "smtp.gmail.com"
password = "DooDooHead"
sender_mail = "mskasan21@gmail.com"
receiver_mail = ["mskasan30@gmail.com"]
pincodes = ["400607"]

for pincode in pincodes:
    to_send_mail = False
    info = cowin.get_availability_by_pincode(pin_code=pincode)
    centers = info["centers"]
    avaliablity_information = {
        "centers": [],
        "type": [],
        "amount": []
    }
    
    for center in centers:
        to_add = {
            "centers": center["name"],
            "type": [],
            "amount": []
        }
        session_info = center["sessions"]
        for session in session_info:
            capacity = session["available_capacity"]
            if not to_send_mail:
                to_send_mail = capacity > 0
            to_add["amount"].append(capacity)
            to_add["type"].append(session["vaccine"])

        for key in to_add.keys():
            avaliablity_information[key].append(to_add[key])

    if to_send_mail:
        context = ssl.create_default_context()
        message_content = f"Pincode: {pincode}<br>"

        for i, center in enumerate(avaliablity_information['centers']):
            new_message = f"Center: {center}<br>Amount:"

            for capacity in avaliablity_information['amount'][i]:
                new_message += f"{capacity}, "
            new_message += "<br>Type:"
            for vac in avaliablity_information['type'][i]:
                new_message += f"{vac}, "

            message_content += f"{new_message}<hr><br>"
        print(message_content)
        message = MIMEMultipart("alternative")
        message["Subject"] = "multipart test"
        message["From"] = sender_mail

        html_message = f"""
            <html>
                <body>
                    {message_content}
                </body>
            </html>
        """

        mimeHTML = MIMEText(html_message, "html")
        message.attach(mimeHTML)
        with smtplib.SMTP_SSL(stmp_host, port, context=context) as server:
            server.login(sender_mail, password)
            for receiver in receiver_mail:
                message["To"] = receiver
                server.sendmail(sender_mail, receiver, message.as_string())
                print(f"mail sent to: {receiver}")
            server.close()