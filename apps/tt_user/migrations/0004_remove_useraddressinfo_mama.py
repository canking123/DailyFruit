# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tt_user', '0003_useraddressinfo_mama'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraddressinfo',
            name='mama',
        ),
    ]
