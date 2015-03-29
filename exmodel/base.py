import six
from django.db.models.base import ModelBase
from django.db import models


_mixin_registry = {}


def extend_model(model_name, mixin):
    """
    Registers a mixin a model_name passed as module.Model
    """
    _mixin_registry.setdefault(model_name, [])
    _mixin_registry[model_name].append(mixin)


def get_app_label(attrs):
    """
    Returns an app_label from attrs
    """
    app_label = None
    try:
        from django.apps import apps
    except ImportError:
        # Django < 1.7
        meta = attrs.get('Meta')
        if meta:
            app_label = getattr(meta, 'app_label', None)
        if not app_label:
            app_label = attrs['__module__'].split('.')[-2]
    else:
        # Django >= 1.7
        app_config = apps.get_containing_app_config(attrs['__module__'])
        if app_config:
            app_label = app_config.label
    return app_label


def get_registered_mixins(name, attrs=None, app_label=None):
    """
    Get all the registered mixins for the model name with either attrs to get
    the app_label or as passed in as an argument
    """
    app_label = app_label or get_app_label(attrs)
    if app_label:
        model_name = '%s.%s' % (app_label, name)
        return _mixin_registry.get(model_name, [])
    return []


def get_mixins_meta(basemeta, mixins):
    """
    Merges meta classes from basemeta and mixin classes
    """
    metas = []
    if len(six.class_types) == 2:
        # we need to add a new style class in the
        # bases otherwise python 2 will raise an error
        metas.append(object)
    for mixin in mixins:
        meta = getattr(mixin, 'Meta', None)
        if meta:
            metas.append(meta)
    if basemeta:
        metas.append(basemeta)
    # just make all those meta classes inherit in to one
    return type('Meta', tuple(metas), {})


def get_mixins_attrs(mixins):
    """
    Merges attributes from all mixins
    """
    attrs = {}
    if mixins:
        # just make all those mixin classes inherit in to one
        Mixin = type('Mixin', tuple(mixins), {})
        for k in dir(Mixin):
            if not k.startswith('__') or k in ['__unicode__', '__str__']:
                attrs[k] = getattr(Mixin, k)
    return attrs


class ModelMeta(ModelBase):
    """
    Modified Model meta class that makes it possible for model classes that use
    this to be extended.
    """
    def __new__(cls, name, bases, attrs):
        mixins = get_registered_mixins(name, attrs)
        basemeta = attrs.get('Meta')
        attrs.update(get_mixins_attrs(mixins))
        attrs['Meta'] = get_mixins_meta(basemeta, mixins)
        return ModelBase.__new__(cls, name, bases, attrs)


class Model(six.with_metaclass(ModelMeta, models.Model)):
    """
    Model class that can be extended by registering mixins that add/change
    fields or methods.
    """
    class Meta:
        abstract = True
