# Generated by Django 3.1.7 on 2021-04-24 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0005_auto_20210420_0002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermembership',
            name='unsubscription_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Date de désabonnement'),
        ),
    ]
