# Generated by Django 4.0.3 on 2022-09-29 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0002_alter_card_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='photo',
            field=models.ImageField(blank=True, max_length=300, null=True, upload_to=''),
        ),
    ]