# Generated by Django 5.0.3 on 2024-03-26 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tf_idf', '0005_words_itf'),
    ]

    operations = [
        migrations.RenameField(
            model_name='words',
            old_name='itf',
            new_name='idf',
        ),
    ]