# Generated by Django 5.0.1 on 2024-08-31 07:12

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
            name='TraineePayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('balance', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('payment_date', models.DateField(default=django.utils.timezone.now)),
                ('trainee', models.ForeignKey(limit_choices_to={'groups__name': 'trainee'}, on_delete=django.db.models.deletion.CASCADE, related_name='trainee_payments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
