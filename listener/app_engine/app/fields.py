from django import forms
from django.core.validators import EMPTY_VALUES

class OurModelChoiceIterator(forms.models.ModelChoiceIterator):
    def __iter__(self):
        if self.field.empty_label is not None:
            yield (u"", self.field.empty_label)
        if self.field.cache_choices:
            if self.field.choice_cache is None:
                self.field.choice_cache = [
                    self.choice(obj) for obj in self.queryset
                ]
            for choice in self.field.choice_cache:
                yield choice
        else:
            for obj in self.queryset:
                yield self.choice(obj)

class OurModelChoiceField(forms.ModelChoiceField):
    """ This required a few modifications to get working on app engine it seems """

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop("model")
        super(OurModelChoiceField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value in EMPTY_VALUES:
            return None
        value = self.model.get(value)
        return value

    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return OurModelChoiceIterator(self)

    choices = property(_get_choices, forms.ModelChoiceField._set_choices)