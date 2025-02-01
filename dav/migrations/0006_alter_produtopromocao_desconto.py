# Generated by Django 5.1.5 on 2025-02-01 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dav', '0005_alter_produtopromocao_desconto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produtopromocao',
            name='desconto',
            field=models.IntegerField(choices=[(5, '5%'), (10, '10%'), (15, '15%'), (20, '20%'), (25, '25%')], default=10),
        ),
    ]
