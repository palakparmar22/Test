from mailersend import emails
import random

global otp
def send_mail(email):    
    mailer = emails.NewEmail('mlsn.73ffe19d34f86a4b11087ae37efc5ece140d05562562c1b98705931aa7d9e282') 
    # mailer = emails.NewEmail('mlsn.10e47c4306004a9fd7c25b8bab74048950d6ed62b0a50496d1f17c81891525be') 

    # define an empty dict to populate with mail values    
    mail_body = {}    
    mail_from = {        
    "name": "Techsture Technologies",        
    "email": "info@trial-351ndgwyryxlzqx8.mlsender.net",    
    # "email": "info@trial-o65qngkk2mdgwr12.mlsender.net",    
    }    
    recipients = [
    {            
        "name": "Test User",
        "email": email,        
    } ]
    
    global otp
    otp = random.randint(1000,9999)
    # print(otp)    

    mailer.set_mail_from(mail_from, mail_body)    
    mailer.set_mail_to(recipients, mail_body)    
    mailer.set_subject("Email Verification", mail_body)    
    mailer.set_html_content(f"OTP for email verification is : {otp}", mail_body)
    
    # using print() will also return status code and data
    print("status code and data: ",mailer.send(mail_body))    
    return otp


# send_mail("palakparmar2282001@gmail.com")

