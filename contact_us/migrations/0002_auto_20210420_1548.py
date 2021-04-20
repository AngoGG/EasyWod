# Generated by Django 3.1.7 on 2021-04-20 13:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contact_us', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmessage',
            name='answer_date',
            field=models.DateField(null=True, verbose_name='Date de réponse'),
        ),
        migrations.AddField(
            model_name='contactmessage',
            name='message_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Date du message'),
            preserve_default=False,
        ),
    ]
