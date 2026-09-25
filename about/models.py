from django.db import models

# Create your models here.
class Product(models.Model):
    BODY_CHOICES = [
        ("Sedan", "Sedan"),
        ("Coupe", "Coupe"),
        ("SUV", "SUV"),
        ("Wagon", "Wagon"),
        ("Liftback", "Liftback"),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    price = models.IntegerField()
    body = models.CharField(max_length=20, choices=BODY_CHOICES, default="Sedan")