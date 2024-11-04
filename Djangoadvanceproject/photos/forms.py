from django import forms

from Djangoadvanceproject.core.form_mixins import ReadonlyFieldsFormMixin
from Djangoadvanceproject.photos.models import ThreeDPhoto


class ThreeDPhotoBaseForm(forms.ModelForm):
    class Meta:
        model = ThreeDPhoto
        fields = ('photo', 'photo_name', 'description', 'photo_tags', 'threedmodels')


class ThreeDPhotoCreateForm(ThreeDPhotoBaseForm):
    pass


class ThreeDPhotoEditForm(ReadonlyFieldsFormMixin, ThreeDPhotoBaseForm):
    class Meta(ThreeDPhotoBaseForm.Meta):
        # Ensure that the photo field is not required
        fields = ('photo', 'photo_name', 'description', 'photo_tags', 'threedmodels')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_readonly_on_fields()

        # Make the photo field optional
        self.fields['photo'].required = False
