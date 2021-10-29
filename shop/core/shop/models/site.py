from django.db.models import CharField,Model

class Site(Model):
    domain = CharField(
        'domain name',
        max_length=100,
        unique=True,
    )
    name = CharField('display name', max_length=50)
    host = CharField(max_length=50,null=True)

    class Meta:
        db_table = 'django_site'
        verbose_name = 'site'
        verbose_name_plural = 'sites'
        ordering = ('domain',)

    def __str__(self):
        return self.domain

    def natural_key(self):
        return (self.domain,)