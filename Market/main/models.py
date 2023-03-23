from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class CustomUser(AbstractUser):
    # Переопределяем стандартного пользователя, теперь у него есть поля ФИО, номер телефона и email
    fio = models.CharField('ФИО', max_length=255)
    email = models.EmailField('Email', unique=True)
    phone = models.CharField('Номер телефона', max_length=20)


class Order(models.Model):
    # Поля заказа: дата создания и пользователь (создаются автоматически)
    creation_date = models.DateField('Дата создания', auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('show_order', kwargs={'order_id': self.pk})

    def get_delete_url(self):
        return reverse('delete_order', kwargs={'order_id': self.pk})

    def get_check_url(self):
        return reverse('order_check', kwargs={'order_id': self.pk})

    def __str__(self):
        return(f'Заказ № {self.pk}')


class Status(models.Model):
    # Поля статуса: сам статус, администратор, дата вердикта, причина отказа или комментарий, заказ, к которому статус относится
    STATUSES = (
        ('Отклонен', 'Отклонен'),
        ('Подтвержден', 'Подтвержден'),
    )

    name = models.CharField(choices=STATUSES, max_length=15)
    admin = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    date = models.DateField(auto_now=True)
    reason = models.TextField()
    order = models.OneToOneField(Order, on_delete=models.CASCADE)

    def get_delete_url(self):
        return reverse('delete_status', kwargs={'status_id': self.pk})

class Product(models.Model):
    # Поля товара: ссылка, название, комментарий и заказа, в котором этот товар лежит
    link = models.CharField('Ссылка', max_length=255)
    name = models.CharField('Название', max_length=255)
    comment = models.TextField('Комментарий', blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def get_delete_url(self):
        return reverse('delete_product', kwargs={'product_id': self.pk})


