# Generated by Django 4.1.7 on 2024-02-29 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_rename_paitent_appointment_patient'),
    ]

    operations = [
        migrations.CreateModel(
            name='PharmacyItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('curr_stock', models.IntegerField(blank=True, null=True)),
                ('category', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
