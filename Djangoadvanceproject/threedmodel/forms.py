from django import forms
from django.core.exceptions import ValidationError

from Djangoadvanceproject.core.form_mixins import ReadonlyFieldsFormMixin
from Djangoadvanceproject.threedmodel.models import Threedmodel


class ThreeDBaseForm(forms.ModelForm):
    class Meta:
        model = Threedmodel
        fields = ("name", "threedmodel_photo")  # Ensure both fields are included

        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Design name", "required": "required"}),  # Ensure required attribute is set
            "threedmodel_photo": forms.ClearableFileInput(attrs={"placeholder": "Upload image", "required": "required"}),  # Ensure required attribute is set
        }

        labels = {
            "name": "3DModel name",
            "threedmodel_photo": "Upload image",
        }


class ThreeDCreateForm(ThreeDBaseForm):
    pass


class ThreeDEditForm(ReadonlyFieldsFormMixin, ThreeDBaseForm):
    class Meta:
        model = Threedmodel
        fields = ['name', 'threedmodel_photo']


class ThreeDDeleteForm(ReadonlyFieldsFormMixin, ThreeDBaseForm):
    readonly_fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_readonly_on_fields()

        for field in self.fields.values():
            field.required = False

    def save(self, commit=True):
        if commit:
            self.instance.delete()
        return self.instance
