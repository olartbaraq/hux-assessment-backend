# Generated by Django 5.0.4 on 2024-04-22 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact_control', '0003_alter_contact_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='phone_number',
            field=models.BigIntegerField(unique=True),
        ),
    ]