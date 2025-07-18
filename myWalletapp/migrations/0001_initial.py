# Generated by Django 5.2.1 on 2025-06-05 14:21

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Category name (e.g. Salary, Rent, Food)', max_length=50, validators=[django.core.validators.MinLengthValidator(2)])),
                ('transaction_type', models.CharField(choices=[('IN', 'Income'), ('EX', 'Expense')], help_text='Income or Expense category', max_length=2)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['transaction_type', 'name'],
                'unique_together': {('user', 'name', 'transaction_type')},
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, help_text='Transaction amount', max_digits=10)),
                ('description', models.CharField(blank=True, help_text='Optional transaction description', max_length=100, null=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('category', models.ForeignKey(help_text='Select or create a category', on_delete=django.db.models.deletion.PROTECT, related_name='transactions', to='myWalletapp.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
                'ordering': ['-date'],
            },
        ),
    ]
