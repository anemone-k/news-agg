from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


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
class Word(models.Model):
    word = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.word

    class Meta:
        ordering = ['word']


class Wordlocation(models.Model):
    word=models.CharField(max_length=250, default='')
    word1 = models.ForeignKey(Word, on_delete=models.CASCADE)
    new = models.ForeignKey(News,on_delete=models.CASCADE)
    location=models.CharField(validators=[ validate_comma_separated_integer_list ], max_length=30)
    tf = models.DecimalField(max_digits=5, decimal_places=4)
    url = models.CharField(max_length=250, default='')
    d = models.IntegerField(default=0)

    def __str__(self):
        return self.word

    class Meta:
        ordering = ['word']

class My_lenta(models.Model):
    lenta_owner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    ria=models.BooleanField(default=False, verbose_name='РИА новости')
    interfax=models.BooleanField(default=False, verbose_name='Interfax')
    regnum=models.BooleanField(default=False, verbose_name='REGNUM')
    rt=models.BooleanField(default=False,verbose_name='RT')

class Likes(models.Model):
    lenta_owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    new = models.ForeignKey(News,on_delete=models.CASCADE)



# Create your models here.

