# Generated by Django 4.0.4 on 2022-06-03 14:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0002_topic_roomy_host_message_roomy_topic'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='roomy',
            options={'ordering': ['-updated', '-created']},
        ),
        migrations.AddField(
            model_name='roomy',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='participants', to=settings.AUTH_USER_MODEL),
        ),
    ]