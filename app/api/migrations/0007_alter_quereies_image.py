# Generated by Django 3.2 on 2021-07-01 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20210630_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quereies',
            name='image',
            field=models.ImageField(upload_to='src/api/classifier'),
        ),
    ]