# Generated by Django 3.2.7 on 2021-09-08 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('turing', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clientes',
            old_name='name_client',
            new_name='name',
        ),
    ]
