from django.db import models

CURRENCY_CHOICES = (('USD', 'usd'), ('RUB', 'rub'),)
CUR_RATE = {'USD': 1, 'RUB': 60.46}


class Item(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название товара')
    description = models.TextField(verbose_name='Описание товара')
    price = models.PositiveIntegerField(
       verbose_name='Цена товара'
    )
    image = models.ImageField(upload_to='products/')
    currency = models.CharField(
        max_length=9, choices=CURRENCY_CHOICES, default='USD'
    )

    def __str__(self):
        return self.name

    def get_price(self):
        return int(self.price * CUR_RATE[self.currency])
