# Generated by Django 4.2 on 2024-08-30 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.CharField(max_length=70, unique=True)),
                ('name', models.CharField(max_length=70)),
                ('contact', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('rechargedate', models.DateField(blank=True, null=True)),
                ('monthlyfees', models.IntegerField()),
                ('balance', models.IntegerField(default=0)),
                ('remarks', models.TextField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pkg_name', models.CharField(max_length=30, unique=True)),
                ('description', models.TextField(blank=True, max_length=25, null=True)),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserRechargeHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(blank=True, max_length=70, null=True)),
                ('recharge_date', models.DateTimeField(auto_now_add=True)),
                ('monthlyfees', models.IntegerField(blank=True, default=0, null=True)),
                ('remarks', models.TextField(blank=True, max_length=100, null=True)),
                ('package', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bookings.package')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.alluser')),
            ],
        ),
        migrations.CreateModel(
            name='UserPaymentLedger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(blank=True, max_length=70, null=True)),
                ('paid_amount', models.IntegerField()),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('paid_by', models.CharField(blank=True, max_length=20, null=True)),
                ('received_by', models.CharField(max_length=20)),
                ('remarks', models.TextField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recharge_histories', to='bookings.alluser')),
            ],
        ),
        migrations.AddField(
            model_name='alluser',
            name='pkg',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bookings.package'),
        ),
    ]
