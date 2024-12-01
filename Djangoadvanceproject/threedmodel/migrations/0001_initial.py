# Generated by Django 4.2.4 on 2024-11-11 11:11

import Djangoadvanceproject.threedmodel.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Threedmodel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('threedmodel_photo', models.ImageField(upload_to='threedmodel_photos/', validators=[Djangoadvanceproject.threedmodel.models.MaxFileSizeValidator(limit_value=12582912)])),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, editable=False, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
