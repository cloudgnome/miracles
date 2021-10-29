from django.db import models

class Language(models.Model):
    code = models.CharField(max_length=5)
    image = models.ImageField(upload_to="lang/")
    name = models.CharField(max_length=20,null=True)
    path = models.CharField(max_length=255,null=True)
    ISOcode = models.CharField(max_length=5,null=True)

    def __str__(self):
        return '%s %s' % (self.name,self.code)

    @property
    def image_url(self):
        try:
            return self.image.url
        except:
            return '/media/data/no_image_new.jpg'

    @property
    def admin_image(self):
        return "<img src='%s'>" % self.image_url