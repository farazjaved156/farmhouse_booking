# Generated by Django 4.2 on 2024-12-01 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='booking',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='farmhouse',
            name='day_shift_price',
        ),
        migrations.RemoveField(
            model_name='farmhouse',
            name='night_shift_price',
        ),
        migrations.CreateModel(
            name='FarmhousePricing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField()),
                ('month', models.CharField(choices=[('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'), ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'), ('09', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')], max_length=2)),
                ('shift', models.CharField(choices=[('day', 'Day Shift (8 AM - 7 PM)'), ('night', 'Night Shift (8 PM - 7 AM)')], max_length=5)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('farmhouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pricing_options', to='listings.farmhouse')),
            ],
            options={
                'verbose_name_plural': 'Farmhouse Pricing Options',
                'unique_together': {('farmhouse', 'year', 'month', 'shift')},
            },
        ),
    ]
