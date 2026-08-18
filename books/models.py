from django.db import models

# Create your models here.v

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    published_date = models.DateField()
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.title