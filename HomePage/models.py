from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=500)
    maker = models.CharField(max_length=500)
    summary = models.TextField()
    slug = models.CharField(max_length=500)
    theme = models.CharField(max_length=10)
    background = models.CharField(max_length=10)

    def __str__(self):
        return self.name
class Subscriber(models.Model):
    email = models.CharField(max_length=500)
    product = models.CharField(max_length=500)
class Maker(models.Model):
    email = models.CharField(max_length=500)
    product = models.CharField(max_length=500) 