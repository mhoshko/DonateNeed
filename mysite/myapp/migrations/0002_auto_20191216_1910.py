# Generated by Django 2.2.8 on 2019-12-16 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request_in_progress',
            name='item',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
