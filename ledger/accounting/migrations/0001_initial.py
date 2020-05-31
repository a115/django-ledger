# Generated by Django 3.0.6 on 2020-05-29 18:53

import accounting.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Entries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=1024)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20, validators=[accounting.models.validate_positive_amount])),
                ('credit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='credit', to='accounting.Account')),
                ('debit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='debit', to='accounting.Account')),
            ],
        ),
        migrations.AddIndex(
            model_name='entries',
            index=models.Index(fields=['credit', 'debit'], name='accounting__credit__aebb13_idx'),
        ),
    ]
