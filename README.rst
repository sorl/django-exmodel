django-exmodel
==============
The ex-model lets you extend models in apps by adding mixins to them.
The mixins can override fields and methods of the original model.

Example::

    # file: staff.models
    from django.db import models
    from exmodel import Model, extend_model


    class Person(Model):
        name = models.CharField(max_length=10)
        room = models.CharField(max_length=10)

        def __unicode__(self):
            return self.name

        class Meta:
            app_label = 'staff'
            verbose_name = 'Person name'


    class PersonMixin(object):
        name = models.CharField(max_length=500)
        alias = models.CharField(max_length=500)

        def __unicode__(self):
            return u'%s (%s)' % (self.name, self.alias)

        class Meta:
            verbose_name = 'Person name and alias'


    extend_model('staff.Person', PersonMixin)


The resulting model will be::

    class Person(Model):
        name = models.CharField(max_length=500)
        room = models.CharField(max_length=10)
        alias = models.CharField(max_length=500)

        def __unicode__(self):
            return u'%s (%s)' % (self.name, self.alias)

        class Meta:
            app_label = 'staff'
            verbose_name = 'Person name'

    extend_model('staff.Person', PersonMixin)
