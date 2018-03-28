# -*- coding: utf-8 -*-



from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voter',
            name='last_sms_status',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
