# Generated by Django 5.0.3 on 2024-03-25 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tf_idf', '0002_alter_words_word'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='words',
            name='idf',
        ),
    ]
