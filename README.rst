django-exmodel
==============
The ex-model lets you extend models in apps by adding mixins to them.
The mixins can override fields and methods of the original model.

``ÌNSTALLED_APPS``::

    ...
    'email_staff',
    'extended_staff',
    'staff',
    ...


``staff.models``::

    from django.db import models
    from exmodel import Model, extend_model


    class Person(Model):
        name = models.CharField(max_length=10)
        room = models.CharField(max_length=10)

        def __unicode__(self):
            return self.name

        class Meta:
            app_label = 'staff'
            verbose_name = u'Person name'


``extended_staff.models``::

    class PersonMixin(object):
        name = models.CharField(max_length=500)
        alias = models.CharField(max_length=500)

        def __unicode__(self):
            return u'%s (%s)' % (self.name, self.alias)

        class Meta:
            verbose_name = u'Person name and alias'


    extend_model('staff.Person', PersonMixin)


``email_staff.models``::

    class PersonEmailMixin(object):
        email = models.EmailField(max_length=500)

        def get_email_address(self):
            return u'%s <%s>' % (self.name, self.email)

    extend_model('staff.Person', PersonEmailMixin)


Now if you do ``from staff.models import Person`` the resulting model will be::

    class Person(Model):
        name = models.CharField(max_length=500)
        room = models.CharField(max_length=10)
        alias = models.CharField(max_length=500)
        email = models.EmailField(max_length=500)

        def __unicode__(self):
            return u'%s (%s)' % (self.name, self.alias)

        def get_email_address(self):
            return u'%s <%s>' % (self.name, self.email)

        class Meta:
            app_label = 'staff'
            verbose_name = 'Person name and alias'
