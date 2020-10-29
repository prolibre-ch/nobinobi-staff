#  Copyright (C) 2020 <Florian Alu - Prolibre - https://prolibre.com
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

# Generated by Django 2.0.13 on 2020-08-05 09:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import nobinobi_staff.models


class Migration(migrations.Migration):

    dependencies = [
        ('nobinobi_staff', '0008_add_partial_disability'),
    ]

    operations = [
        migrations.AlterField(
            model_name='absence',
            name='abs_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='nobinobi_staff.AbsenceType', verbose_name="Absence Type"),
        ),
    ]
