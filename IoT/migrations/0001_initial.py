# Generated by Django 2.0.4 on 2018-07-12 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
    ]
