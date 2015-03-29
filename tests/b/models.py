from django.db import models
from exmodel import extend_model


class AMixin(object):
    b = models.BooleanField(default=True)
    c = 2

    class Meta:
        verbose_name_plural = 'me'
        ordering = ('b',)

extend_model('a.A', AMixin)
