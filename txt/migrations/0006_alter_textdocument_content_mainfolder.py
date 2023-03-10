# Generated by Django 4.1 on 2023-01-12 07:20

import ckeditor.fields
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('txt', '0005_alter_textdocument_date_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textdocument',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.CreateModel(
            name='MainFolder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('files', models.ManyToManyField(to='txt.textdocument')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
