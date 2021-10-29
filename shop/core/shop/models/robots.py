from django.db.models import Model,OneToOneField,CharField,BooleanField

class Robots(Model):
    body = CharField(max_length=1000,verbose_name='Текст')
    mobile = BooleanField(default=0)

    @property
    def is_mobile(self):
        return '<div class="bool %s"></div>' % str(self.mobile).lower()

    def __str__(self):
        return 'Robots {}'.format(self.id)

    class Meta:
        verbose_name = 'robots'
        verbose_name_plural = 'robots'