# Generated by Django 4.0.6 on 2022-08-08 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_rent', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
