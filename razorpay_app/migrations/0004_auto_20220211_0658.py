# Generated by Django 3.2.11 on 2022-02-11 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('razorpay_app', '0003_remove_payment_razorpay_payment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='razorpay_payment_id',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='payment',
            name='order_id',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
