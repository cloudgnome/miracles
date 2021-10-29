from django.db.models import Model,CharField

class Redirect(Model):
    old_path = CharField(max_length=255,unique=True)
    new_path = CharField(max_length=255,null=True)