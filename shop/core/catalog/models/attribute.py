from django.db.models import Model,CharField,ForeignKey,CASCADE,ManyToManyField
from catalog.models import Category

class Attribute(Model):
    name = CharField(max_length=50,verbose_name="Название",unique=True)
    category = ManyToManyField(Category,related_name="attributes")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Атрибут"

class Value(Model):
    attribute = ForeignKey(Attribute,related_name="values", on_delete=CASCADE)
    value = CharField(max_length=255,verbose_name="Значение")

    def __str__(self):
        return self.value

    def name(self):
        return self.attribute.name

    class Meta:
        verbose_name = "Значение"
        ordering = ['value']