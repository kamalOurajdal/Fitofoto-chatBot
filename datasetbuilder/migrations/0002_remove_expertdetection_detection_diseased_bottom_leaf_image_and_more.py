# Generated by Django 4.1.7 on 2023-06-02 03:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasetbuilder', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expertdetection',
            name='detection_diseased_bottom_leaf_image',
        ),
        migrations.RemoveField(
            model_name='expertdetection',
            name='detection_diseased_top_leaf_image',
        ),
    ]
