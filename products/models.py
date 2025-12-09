from django.db import models

class Product(models.Model):
    name = models.CharField("Название", max_length=200)
    description = models.TextField("Описание", blank=True)
    price = models.DecimalField("Цена", max_digits=8, decimal_places=2)
    image = models.ImageField("Фото", upload_to="products/", blank=True)
    in_stock = models.BooleanField("В наличии", default=True)
    stock = models.PositiveIntegerField("Количество на складе", default=0)  


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жидкость"
        verbose_name_plural = "Жидкости"
