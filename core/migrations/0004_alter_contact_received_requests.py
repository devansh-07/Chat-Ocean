# Generated by Django 3.2.4 on 2021-06-11 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210611_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='received_requests',
            field=models.ManyToManyField(blank=True, related_name='received', to='core.Contact'),
        ),
    ]
