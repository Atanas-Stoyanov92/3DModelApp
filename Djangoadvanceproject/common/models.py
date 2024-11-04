from django.contrib.auth import get_user_model
from django.db import models

from Djangoadvanceproject.photos.models import ThreeDPhoto

UserModel = get_user_model()


# Create your models here.
class PhotoComment(models.Model):
    MAX_TEXT_LENGTH = 300

    text = models.TextField(
        max_length=MAX_TEXT_LENGTH,
        null=False,
        blank=False,
    )

    created_at = models.DateTimeField(
        auto_now=True,
    )

    threed_photo = models.ForeignKey(
        ThreeDPhoto,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        UserModel, on_delete=models.RESTRICT)


class PhotoLike(models.Model):
    threed_photo = models.ForeignKey(
        ThreeDPhoto,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        UserModel, on_delete=models.RESTRICT)
