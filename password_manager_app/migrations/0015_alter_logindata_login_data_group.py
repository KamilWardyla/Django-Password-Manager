# Generated by Django 4.1.2 on 2022-11-03 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('password_manager_app', '0014_alter_secretnote_note_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logindata',
            name='login_data_group',
            field=models.PositiveSmallIntegerField(choices=[('Web Application Password', 'Web Application Password'), ('Mail Account', 'Mail Account'), ('Online Identies', 'Online Identies'), ('Social Media', 'Social Media'), ('Financial Record', 'Financial Record'), ('Desktop App', 'Desktop App'), ('Mobie App', 'Mobie App')]),
        ),
    ]