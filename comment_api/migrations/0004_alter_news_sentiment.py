# Generated by Django 5.1.6 on 2025-03-12 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment_api', '0003_news'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='sentiment',
            field=models.CharField(blank=True, choices=[('Positive', 'Positive'), ('Negative', 'Negative'), ('Neutral', 'Neutral')], max_length=8, null=True),
        ),
    ]
