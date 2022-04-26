from django.db import models

# Create your models here.

class Test(models.Model):
    content = models.CharField(max_length=200)
    visitor = models.CharField(max_length=20)
    email = models.EmailField(max_length=20)
    date_time = models.DateTimeField()
    