# Generated by Django 3.2.5 on 2021-12-06 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_collectors', '0007_auto_20211201_0002'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collectionitem',
            options={'ordering': ['id']},
        ),
    ]