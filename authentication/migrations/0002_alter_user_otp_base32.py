# Generated by Django 5.2 on 2025-04-20 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='otp_base32',
            field=models.CharField(blank=True, default='2OXNNVZUMFHGP4UYTSMUYD2CKP2M73ZN', max_length=64),
        ),
    ]
