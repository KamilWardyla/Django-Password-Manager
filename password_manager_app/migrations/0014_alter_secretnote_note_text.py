# Generated by Django 4.1.2 on 2022-11-02 14:23

from django.db import migrations
import encrypted_model_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('password_manager_app', '0013_rename_case_topic_supportcontact_topic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='secretnote',
            name='note_text',
            field=encrypted_model_fields.fields.EncryptedTextField(),
        ),
    ]