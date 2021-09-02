# Generated by Django 3.2 on 2021-09-01 22:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Wants',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('want', models.CharField(blank=True, max_length=1000, null=True)),
                ('manifested_on', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
            ],
            options={
                'db_table': 'wants',
            },
        ),
    ]