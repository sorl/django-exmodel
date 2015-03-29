from django.db import models
from exmodel import Model


class A(Model):
    a = models.CharField(max_length=1)
    b = models.CharField(max_length=1)
    c = 1

    class Meta:
        verbose_name = 'who'
        ordering = ('a',)
