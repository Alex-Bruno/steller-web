# Generated by Django 2.2.7 on 2020-02-20 00:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accessApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Access',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plate', models.CharField(blank=True, max_length=12, null=True, verbose_name='Placa')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('entrance', models.DateTimeField(blank=True, null=True, verbose_name='Entrada')),
                ('exit', models.DateTimeField(blank=True, null=True, verbose_name='Saída')),
                ('active', models.BooleanField(default=True)),
                ('vehicle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='access', to='accessApp.Vehicle')),
            ],
            options={
                'ordering': ('-created',),
                'verbose_name': 'Acesso',
                'verbose_name_plural': 'Acessos',
            },
        ),
    ]
