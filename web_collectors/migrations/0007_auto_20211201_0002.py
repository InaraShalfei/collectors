# Generated by Django 3.2.5 on 2021-11-30 18:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web_collectors', '0006_auto_20211130_1549'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collectionitem',
            options={},
        ),
        migrations.AlterModelOptions(
            name='photo',
            options={},
        ),
        migrations.RemoveField(
            model_name='collectionitem',
            name='photo',
        ),
        migrations.RemoveField(
            model_name='collectionitem',
            name='position',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='photo',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='position',
        ),
        migrations.AddField(
            model_name='photo',
            name='file',
            field=models.FileField(default='her', upload_to='media/', verbose_name='Photo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='photo',
            name='item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='web_collectors.collectionitem'),
            preserve_default=False,
        ),
    ]
