import random
from django.conf import settings
from django.core.mail import send_mail
import smtplib 


MYEMAIL ='neuronerdsexplain@gmail.com'

def gen_otp_six_digit():
    return str(random.randint(100000,999999))


def send_otp_email(email,otp):
    mail_server = smtplib.SMTP('smtp.gmail.com',587)
    mail_server.starttls()
    mail_server.login(MYEMAIL,'zgrafmoaqcwhzrgb')
    message = f"your otp is {otp}. \n Don't share this with anyone" 
    mail_server.sendmail(MYEMAIL,email,message)
    
   
def send_password_reset(email,link):
    mail_server = smtplib.SMTP('smtp.gmail.com',587)
    mail_server.starttls()
    mail_server.login(MYEMAIL,'zgrafmoaqcwhzrgb')
    message = f"your password reset link is\n{link}\n\n\nDon't share with anyone also it expire after 10 minutes"
    mail_server.sendmail(MYEMAIL,email,message)