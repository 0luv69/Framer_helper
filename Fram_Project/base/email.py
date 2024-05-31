from django.conf import settings
from django.core.mail import send_mail




def send_account_activation_email(email, email_token, user):
    subject= 'lets verify so click the link plz'
    email_from = settings.EMAIL_HOST_USER
    message = f'''Hi, {user.username} Your authentation url is plz open to be verified user, thank
    click on the link to Activate Your account http:localhost:8000/auth/activate/{email_token}
    thanks
'''

    send_mail(subject, message, email_from, [email])

