# Generated by Django 4.1.2 on 2022-10-26 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('password_manager_app', '0003_alter_secretnote_note_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='secretnote',
            name='note_text',
            field=models.TextField(),
        ),
    ]
