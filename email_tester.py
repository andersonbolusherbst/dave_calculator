from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, ssl  ### need to add these imports tio the main streamlit file and to the requirements
def send_email(monthly,m,escalation,amounts,years,max_contribution=None,currency_selector=None):
    
    
    
    
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "bayswatercalculator@gmail.com"  # Enter your address
    receiver_email = "lukeherbst2@gmail.com"  # Enter receiver address
    password = "wciivablmetkkfdu"
    
    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    
    text = f"""
    Thanks for using Bayswater Calculator:
    Your calculation came up with the following:
    
     If you invest **{monthly}** {currency_selector}, **{m}** times a year with an annual escalation of 
    **{escalation}**, your investment will generate **{amounts[-1]}** **{currency_selector}** in **{years}** years
    visit bayswatercapital.co.za for more info, or phone your main man Danger Dave: 09898731948
    """
    html = f"""
    <html>
        <body>
            <p>Hi,<br>
                Thanks for using Bayswater Calculator? <br>
                If you invest <b>{monthly}{currency_selector}</b>, <b>{m}</b> times a year with an annual escalation of 
                <b>{escalation}</b>, your investment will generate <b>{amounts[-1]}</b> <b>{currency_selector}</b> in <b>{years}</b> years
                 <img src="C:/Users/Luke/Documents/GitHub/dave_calculator/dave_calculator/visualization.png" alt="Graph">
                 visit  <a href="http://www.bayswatercapital.co.za">Bayswatercapital</a> <br>
                for more info, or phone your main man Danger Dave: 09898731948             
                
            </p>
        </body>
    </html>
    """
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    #  The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        #decimal_data = final_data.iloc[:, 0]
        #decimal_data = np.round(decimal_data, decimals = 2)
#send_email(1,2,3,[4],5,"max contrinution","USD")

