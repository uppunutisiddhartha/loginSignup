# Generated by Django 5.1.1 on 2024-10-11 16:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_note_options_alter_note_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='book',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='base.book'),
            preserve_default=False,
        ),
    ]