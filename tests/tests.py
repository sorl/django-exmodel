from unittest import TestCase
from exmodel.base import get_mixins_meta, get_mixins_attrs
from exmodel.base import extend_model, get_registered_mixins
from exmodel import base
from django.db import models


class MixinA(object):
    a = models.CharField(max_length=1)

    def __str__(self):
        pass

    class Meta:
        verbose_name = 'A'


class MixinB(object):
    b = models.TextField()

    class Meta:
        verbose_name_plural = 'B'


class MixinC(object):
    a = 'a'
    c = models.BooleanField()

    class Meta:
        verbose_name = 'C'
        verbose_name_plural = 'C'
        ordering = ('c',)


class Meta:
    ordering = ('xyz',)


mixins_a = [MixinA]
mixins_b = [MixinB, MixinA]
mixins_c = [MixinC, MixinB, MixinA]


class BaseTestCase(TestCase):
    def test_a(self):
        attrs = get_mixins_attrs(mixins_a)
        self.assertTrue(isinstance(attrs['a'], models.CharField))
        self.assertTrue(attrs.get('__str__'))

    def test_b(self):
        attrs = get_mixins_attrs(mixins_b)
        self.assertTrue(isinstance(attrs['a'], models.CharField))
        self.assertTrue(attrs.get('__str__'))
        self.assertTrue(isinstance(attrs['b'], models.TextField))

    def test_c(self):
        attrs = get_mixins_attrs(mixins_c)
        self.assertEqual(attrs['a'], 'a')
        self.assertTrue(attrs.get('__str__'))
        self.assertTrue(isinstance(attrs['b'], models.TextField))
        self.assertTrue(isinstance(attrs['c'], models.BooleanField))

    def test_a_meta(self):
        meta = get_mixins_meta(Meta, mixins_a)
        self.assertEqual(meta.ordering, ('xyz',))
        self.assertEqual(meta.verbose_name, 'A')

    def test_b_meta(self):
        meta = get_mixins_meta(Meta, mixins_b)
        self.assertEqual(meta.ordering, ('xyz',))
        self.assertEqual(meta.verbose_name, 'A')
        self.assertEqual(meta.verbose_name_plural, 'B')

    def test_c_meta(self):
        meta = get_mixins_meta(Meta, mixins_c)
        self.assertEqual(meta.ordering, ('c',))
        self.assertEqual(meta.verbose_name, 'C')
        self.assertEqual(meta.verbose_name_plural, 'C')


class RegisterTestCase(TestCase):
    def setUp(self):
        base._mixin_registry = {}

    def test_register(self):
        extend_model('app.model', MixinA)
        self.assertEqual(
            get_registered_mixins('model', app_label='app')[0],
            MixinA
        )

    def test_register_a3(self):
        extend_model('app.model', MixinA)
        extend_model('app.model', MixinB)
        extend_model('app.model', MixinC)
        self.assertEqual(
            get_registered_mixins('model', app_label='app')[2],
            MixinC
        )
