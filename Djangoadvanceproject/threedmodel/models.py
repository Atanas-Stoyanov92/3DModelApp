from django.contrib.auth import get_user_model
from django.core.validators import BaseValidator
from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from Djangoadvanceproject.core.models import IHaveUser
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


class Threedmodel(IHaveUser, models.Model):
    MAX_NAME_LENGTH = 30

    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        null=False,
        blank=False,
    )

    threedmodel_photo = models.ImageField(
        upload_to='threedmodel_photos/',
        null=False,
        blank=False,
        validators=(
            # validate_image_size_less_than_5mb,
            MaxFileSizeValidator(limit_value=SIZE_12_MB),
        )
    )

    created_at = models.DateTimeField(
        auto_now=True,
    )

    slug = models.SlugField(
        unique=True,
        null=False,
        blank=True,
        editable=False,  # Readonly, only in the Django App, not in the DB
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.slug:  # slugify("My name") -> "My-name"
            self.slug = slugify(f"{self.name}-{self.pk}")

        super().save(*args, **kwargs)
