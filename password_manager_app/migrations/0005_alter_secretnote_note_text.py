# Generated by Django 4.1.2 on 2022-10-26 18:49

from django.db import migrations
import encrypted_model_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('password_manager_app', '0004_alter_secretnote_note_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='secretnote',
            name='note_text',
            field=encrypted_model_fields.fields.EncryptedCharField(),
        ),
    ]
