from django.db.models import Q
from user.models import User
from main.models import *
from main.forms import *
from base64 import b64decode
from json import loads
from django.core.files.base import ContentFile

class ContentView:
    initial = {}

    def to_file(self,image_file):
        if image_file:

            try:
                if 'data:image/jpeg;base64' in image_file:
                    return ContentFile(b64decode(image_file.replace('data:image/jpeg;base64,','')), name='{}.{}'.format(image_file[27:42],'jpg'))
                elif 'data:image/png;base64' in image_file:
                    return ContentFile(b64decode(image_file.replace('data:image/png;base64,','')), name='{}.{}'.format(image_file[27:42],'png'))
            except Exception as e:
                return