# Generated by Django 5.1.3 on 2024-12-01 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TurfAPP', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productdetail',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
