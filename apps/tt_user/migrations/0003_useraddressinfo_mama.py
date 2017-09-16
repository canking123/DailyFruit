# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tt_user', '0002_auto_20170910_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddressinfo',
            name='mama',
            field=models.CharField(default=1, max_length=5),
            preserve_default=False,
        ),
    ]
