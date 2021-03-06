"""
``autocomplete_light.contrib.generic_m2m`` couples django-autocomplete-light
with django-generic-m2m.

Generic many to many are supported since 0.5. It depends on `django-generic-m2m
<http://django-generic-m2m.rtfd.org>`_ external apps. Follow django-generic-m2m
installation documentation, but at the time of writing it barely consists of
adding the ``genericm2m`` to ``INSTALLED_APPS``, and adding a field to models
that should have a generic m2m relation. So, kudos to the maintainers of
django-generic-m2m, fantastic app, use it for generic many to many relations.

See examples in ``test_project/generic_m2m_example``.
"""
from genericm2m.models import RelatedObjectsDescriptor

from ..generic import GenericForeignKeyField, GenericModelForm


class GenericModelForm(GenericModelForm):
    """
    Extension of autocomplete_light.GenericModelForm, that handles
    genericm2m's RelatedObjectsDescriptor.
    """

    def __init__(self, *args, **kwargs):
        """
        Add related objects to initial for each generic m2m field.
        """
        super(GenericModelForm, self).__init__(*args, **kwargs)

        for name, field in self.generic_m2m_fields():
            related_objects = getattr(self.instance, name).all()
            self.initial[name] = [x.object for x in related_objects]

    def generic_m2m_fields(self):
        """
        Yield name, field for each RelatedObjectsDescriptor of the model of
        this ModelForm.
        """
        for name, field in self.fields.items():
            if not isinstance(field, GenericManyToMany):
                continue

            model_class_attr = getattr(self._meta.model, name, None)
            if not isinstance(model_class_attr, RelatedObjectsDescriptor):
                continue

            yield name, field

    def save(self, commit=True):
        """
        Sorry guys, but we have to force commit=True and call save_m2m() right
        after.

        The reason for that is that Django 1.4 kind of left over cases where we
        wanted to override save_m2m: it enforces its own, which does not care
        of generic_m2m of course.
        """
        model = super(GenericModelForm, self).save(True)
        self.save_m2m()
        return model

    def save_m2m(self):
        """
        Save selected generic m2m relations.
        """
        if hasattr(super(GenericModelForm, self), 'save_m2m'):
            # forward compatibility:
            # Django's ModelForm **should** allow a user to overload the
            # save_m2m method. As of Django 1.4, it still enforces it's own
            # save_m2m function...
            super(GenericModelForm, self).save_m2m()

        for name, field in self.generic_m2m_fields():
            model_attr = getattr(self.instance, name)
            selected_relations = self.cleaned_data.get(name, [])

            for related in model_attr.all():
                if related.object not in selected_relations:
                    model_attr.remove(related)

            for related in selected_relations:
                model_attr.connect(related)


class GenericManyToMany(GenericForeignKeyField):
    """
    Simple form field that converts strings to models.
    """
    def prepare_value(self, value):
        if hasattr(value, '__iter__'):
            return [super(GenericManyToMany, self).prepare_value(v) \
                for v in value]
        return super(GenericManyToMany, self).prepare_value(value)

    def to_python(self, value):
        if hasattr(value, '__iter__'):
            return [super(GenericManyToMany, self).to_python(v) for v in value]
        return super(GenericManyToMany, self).to_python(value)
