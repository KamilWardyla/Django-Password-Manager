# Generated by Django 4.1.2 on 2022-11-04 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('password_manager_app', '0018_alter_creditcard_card_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supportcontact',
            name='sender_name',
        ),
        migrations.AddField(
            model_name='supportcontact',
            name='sender_email',
            field=models.EmailField(default=3, max_length=254),
            preserve_default=False,
        ),
    ]
