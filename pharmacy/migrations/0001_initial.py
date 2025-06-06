# Generated by Django 5.2 on 2025-04-20 09:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderedMedicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('price_per_unit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount_per_unit', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('is_replaced', models.BooleanField(default=False)),
                ('replacement_reason', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pharmacy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('pharmacy_type', models.CharField(choices=[('RETAIL', 'Retail Pharmacy'), ('HOSPITAL', 'Hospital Pharmacy'), ('CHAIN', 'Chain Pharmacy'), ('ONLINE', 'Online Pharmacy')], max_length=20)),
                ('license_number', models.CharField(max_length=100, unique=True)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=17)),
                ('email', models.EmailField(max_length=254)),
                ('is_active', models.BooleanField(default=True)),
                ('operating_hours', models.JSONField()),
                ('delivery_radius_km', models.PositiveIntegerField(default=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Pharmacies',
            },
        ),
        migrations.CreateModel(
            name='PharmacyEarning',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('payment_method', models.CharField(max_length=50)),
                ('status', models.CharField(default='PENDING', max_length=20)),
                ('notes', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PharmacyStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MedicineOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('PROCESSING', 'Processing'), ('READY_FOR_PICKUP', 'Ready for Pickup'), ('OUT_FOR_DELIVERY', 'Out for Delivery'), ('DELIVERED', 'Delivered'), ('CANCELLED', 'Cancelled'), ('REJECTED', 'Rejected')], default='PENDING', max_length=20)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('delivery_address', models.TextField()),
                ('delivery_phone', models.CharField(max_length=17)),
                ('payment_method', models.CharField(choices=[('CASH', 'Cash on Delivery'), ('ONLINE', 'Online Payment'), ('INSURANCE', 'Insurance')], max_length=20)),
                ('payment_status', models.CharField(default='PENDING', max_length=20)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('final_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('delivery_charge', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('expected_delivery_date', models.DateTimeField(blank=True, null=True)),
                ('delivered_at', models.DateTimeField(blank=True, null=True)),
                ('delivery_otp', models.CharField(blank=True, max_length=6)),
                ('notes', models.TextField(blank=True)),
                ('status_hashmap', models.JSONField(default=dict)),
                ('delivery_person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deliveries', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medicine_orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
