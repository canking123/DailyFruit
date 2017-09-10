# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tt_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddressinfo',
            name='uaddress',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='useraddressinfo',
            name='uphone',
            field=models.CharField(max_length=11),
        ),
    ]
