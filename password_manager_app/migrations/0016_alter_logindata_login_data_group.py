# Generated by Django 4.1.2 on 2022-11-03 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('password_manager_app', '0015_alter_logindata_login_data_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logindata',
            name='login_data_group',
            field=models.CharField(choices=[('Web Application Password', 'Web Application Password'), ('Mail Account', 'Mail Account'), ('Online Identies', 'Online Identies'), ('Social Media', 'Social Media'), ('Financial Record', 'Financial Record'), ('Desktop App', 'Desktop App'), ('Mobie App', 'Mobie App')], max_length=32),
        ),
    ]