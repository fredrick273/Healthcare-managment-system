# Generated by Django 4.1.7 on 2024-02-08 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_dept_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='Marital_Status',
            field=models.CharField(blank=True, choices=[('Unmarried', 'Unmarried'), ('Married', 'Married'), ('Divorced', 'Divorced')], max_length=100, null=True),
        ),
    ]
