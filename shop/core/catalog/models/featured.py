from django.db import models
from catalog.models import Product,Category

class Featured(models.Model):
    products = models.ManyToManyField(Product,related_name="related")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __iter__(self):
        for product in self.products.all():
            yield product

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        for product in Product.objects.filter(category=self.category):
            product.cached = False
            product.update()

    class Meta:
        verbose_name = "Рекомендуемые наборы"