# Generated by Django 3.1.7 on 2021-04-12 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0002_auto_20210307_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermembership',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.DeleteModel(
            name='Subscription',
        ),
    ]