from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, BaseValidator
from django.db import models

from Djangoadvanceproject.threedmodel.models import Threedmodel

UserModel = get_user_model()

SIZE_12_MB = 12 * 1024 * 1024


class MaxFileSizeValidator(BaseValidator):
    def clean(self, x):
        return x.size

    def compare(self, file_size, max_size):
        return max_size < file_size


def validate_image_size_less_than_12mb(value):
    if value.size > SIZE_12_MB:
        raise ValidationError('File size should be less than 12MB')


class ThreeDPhoto(models.Model):
    MIN_DESCRIPTION_LENGTH = 10
    MAX_DESCRIPTION_LENGTH = 300

    MAX_PHOTO_TAGS_LENGTH = 30
    MAX_PHOTO_NAME_LENGTH = 30

    photo = models.ImageField(
        upload_to='threed_photos',
        blank=False,
        null=False,
        validators=(
            # validate_image_size_less_than_5mb,
            MaxFileSizeValidator(limit_value=SIZE_12_MB),
        )
    )

    photo_name = models.CharField(
        max_length=MAX_PHOTO_NAME_LENGTH,
        null=True,
        blank=True,
    )

    description = models.TextField(
        blank=True,
        null=True,
        max_length=MAX_DESCRIPTION_LENGTH,
        validators=(
            MinLengthValidator(MIN_DESCRIPTION_LENGTH),
        )
    )

    photo_tags = models.CharField(
        max_length=MAX_PHOTO_TAGS_LENGTH,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,  # Done only on `create`
    )

    modified_at = models.DateTimeField(
        auto_now=True,  # On every save
    )

    threedmodels = models.ManyToManyField(Threedmodel)

    user = models.ForeignKey(UserModel,
                             on_delete=models.RESTRICT)

