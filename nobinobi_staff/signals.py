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

import datetime

import arrow
from datetimerange import DateTimeRange
from django.core.management import call_command
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone

from nobinobi_staff.models import Staff, Training, RightTraining, Absence


def create_training_for_staff(instance: Staff, absence: Absence = None):
    dates = []
    if not absence:
        dates.append(timezone.localdate())
    else:
        date = absence.datetime_range
        for value in date.range(datetime.timedelta(days=1)):
            if value.month not in dates:
                dates.append(value)

    rt = RightTraining.objects.first()
    # +1 for accept 12 in range
    if rt:
        training_to_create = []
        for date in dates:
            if date.month in range(rt.start_month, 13):
                start_date = datetime.date(date.year, rt.start_month, rt.start_day)
            else:
                start_date = datetime.date(date.year - 1, rt.start_month, rt.start_day)
            end_date = arrow.get(start_date).shift(years=1, days=-1).date()
            if (start_date, end_date) not in training_to_create:
                training_to_create.append((start_date, end_date))

        for tr_to_create in training_to_create:
            training, created = Training.objects.get_or_create(
                staff=instance,
                start_date=tr_to_create[0],
                end_date=tr_to_create[1],
            )
            if created:
                ta = instance.percentage_work
                training.default_number_days = (rt.number_days * ta) / 100
                training.save()


@receiver(post_save, sender=Staff)
def update_training_for_staff(sender, instance, created, raw, using, **kwargs):
    create_training_for_staff(instance)
    year = timezone.localdate().year
    call_command('update_training', years=[year], staffs=[instance.id])


@receiver(post_save, sender=Absence)
def create_training_for_staff_after_absence(sender, instance, created, raw, using, **kwargs):
    create_training_for_staff(instance.staff, instance)


@receiver((post_save, post_delete), sender=Absence)
def update_training_for_staff_after_absence(sender, instance, **kwargs):
    if instance.abs_type.abbr == "FOR":
        absence_range = instance.datetime_range
        old_absence_start_date = instance.tracker.previous("start_date")
        old_absence_end_date = instance.tracker.previous("end_date")
        old_absence_range = DateTimeRange(old_absence_start_date, old_absence_end_date)

        years = []
        rt = RightTraining.objects.first()
        if rt:
            for value in absence_range.range(datetime.timedelta(days=1)):
                if value.month in range(rt.start_month, 13):
                    year = value.year
                else:
                    year = value.year - 1
                if year not in years:
                    years.append(year)
            if old_absence_start_date and old_absence_end_date:
                for value in old_absence_range.range(datetime.timedelta(days=1)):
                    if value.month in range(rt.start_month, 13):
                        year = value.year
                    else:
                        year = value.year - 1
                    if year not in years:
                        years.append(year)

            call_command('update_training', years=years, staffs=[instance.staff.id])
