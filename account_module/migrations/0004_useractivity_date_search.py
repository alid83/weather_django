# Generated by Django 5.0.7 on 2024-07-29 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_module', '0003_rename_date_useractivity_date_joined_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='useractivity',
            name='date_search',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
