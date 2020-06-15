from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from django.utils import timezone


class News(models.Model):
    url = models.CharField(max_length=250, unique=True)
    title = models.CharField(max_length=250, unique=True)
    data = models.TextField()
    source = models.CharField(max_length=30, default='ria')
    created_date = models.DateTimeField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']

    class Admin:
        pass
# Create your models here.
