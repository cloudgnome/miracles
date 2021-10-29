from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMultiAlternatives
from user.models import User
from django.template.loader import render_to_string
from settings import BASE_URL

class Command(BaseCommand):
    help = 'Send Emails'
    template = 'igroteka/email.html'

    def handle(self, *args, **options):
        users = [User.objects.filter(email='icloudgnome@gmail.com').first(),User.objects.filter(email='4vitaly@mail.ru').first(),User.objects.filter(email='slavikair2013@gmail.com').first()]
        subject, from_email = 'Каталки толокары', "%s Интернет магазин <info@%s>" % (BASE_URL,BASE_URL)
        html_content = text_content = render_to_string(self.template,{})
        for user in users:
            msg = EmailMultiAlternatives(subject, text_content, from_email, [user.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()