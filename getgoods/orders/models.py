from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q


class Shop(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    filename = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'


class Category(models.Model):
    shops = models.ManyToManyField(Shop)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория поставщика'
        verbose_name_plural = 'Категории поставщиков'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def get_info(self):
        return ProductInfo.objects.filter(product=self)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.FloatField()
    price_rrc = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Информация о товаре'
        verbose_name_plural = 'Информация о товарах'


class Parameter(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'


class ProductParameter(models.Model):
    product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.product_info

    class Meta:
        verbose_name = 'Характеристика товара'
        verbose_name_plural = 'Характеристики товаров'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dt = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=[
        ('1', 'one'),
        ('2', 'two'),
        ('3', 'three')
    ])

    def __str__(self):
        return f'order: {self.user.username} / {self.dt} / {self.status}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    @property
    def price(self):
        product_info = ProductInfo.objects.filter(Q(product=self.product) | Q(shop=self.shop)).last()
        if product_info is not None:
            return product_info.price

    @property
    def sum(self):
        price = self.price
        if price is not None:
            return price*self.quantity

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'


class Contact(models.Model):
    type = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    @classmethod
    def get_user_contacts(cls, user):
        return Contact.objects.filter(user=user)

    def __str__(self):
        return f'{self.user.username} / {self.type}'

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_as_username = models.EmailField(max_length=150, unique=True)
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)