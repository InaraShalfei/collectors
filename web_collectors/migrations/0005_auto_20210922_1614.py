# Generated by Django 3.2.5 on 2021-09-22 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_collectors', '0004_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='collectionitem',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]