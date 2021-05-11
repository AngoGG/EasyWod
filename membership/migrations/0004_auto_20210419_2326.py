# Generated by Django 3.1.7 on 2021-04-19 21:26

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0003_auto_20210412_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermembership',
            name='subscribtion_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 19, 21, 26, 13, 812444, tzinfo=utc), verbose_name="Date d'abonnement"),
        ),
        migrations.AddField(
            model_name='usermembership',
            name='unsubscription_date',
            field=models.DateTimeField(null=True, verbose_name='Date de désabonnement'),
        ),
    ]
