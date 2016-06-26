# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-26 19:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=3)),
                ('used', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='IgorItemClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1)),
                ('description', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=3)),
                ('label', models.CharField(blank=True, default=b'', max_length=64)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='SubProductLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=30)),
                ('igor_or_sub_pl', models.CharField(max_length=3)),
                ('label', models.CharField(blank=True, default=b'', max_length=64)),
                ('igorclass', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hierarchy.IgorItemClass')),
            ],
        ),
        migrations.CreateModel(
            name='Usage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='BusinessUnit',
            fields=[
                ('parent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hierarchy.Parent')),
            ],
            bases=('hierarchy.parent',),
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('parent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hierarchy.Parent')),
            ],
            bases=('hierarchy.parent',),
        ),
        migrations.CreateModel(
            name='ProductLine',
            fields=[
                ('parent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hierarchy.Parent')),
            ],
            bases=('hierarchy.parent',),
        ),
        migrations.CreateModel(
            name='ProductLineGroup',
            fields=[
                ('parent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hierarchy.Parent')),
            ],
            bases=('hierarchy.parent',),
        ),
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('parent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hierarchy.Parent')),
            ],
            bases=('hierarchy.parent',),
        ),
        migrations.CreateModel(
            name='SubBusinessUnit',
            fields=[
                ('parent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hierarchy.Parent')),
                ('fbusinessunit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hierarchy.BusinessUnit')),
            ],
            bases=('hierarchy.parent',),
        ),
        migrations.AddField(
            model_name='subproductline',
            name='usage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hierarchy.Usage'),
        ),
        migrations.AddField(
            model_name='subproductline',
            name='fproductline',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hierarchy.ProductLine'),
        ),
        migrations.AddField(
            model_name='productlinegroup',
            name='fsubbusinessunit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hierarchy.SubBusinessUnit'),
        ),
        migrations.AddField(
            model_name='productline',
            name='fproductlinegroup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hierarchy.ProductLineGroup'),
        ),
        migrations.AddField(
            model_name='division',
            name='fsegment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hierarchy.Segment'),
        ),
        migrations.AddField(
            model_name='businessunit',
            name='fdivision',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hierarchy.Division'),
        ),
    ]
