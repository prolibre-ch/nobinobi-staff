import datetime

import arrow
from datetimerange import DateTimeRange
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.timezone import make_aware, make_naive

from nobinobi_staff.models import Staff, Training, RightTraining, Absence


@receiver(post_save, sender=Staff)
def update_training_for_staff(sender, instance, created, raw, using, **kwargs):
    now = timezone.localdate()
    rt = RightTraining.objects.first()
    if rt:
        training, created = Training.objects.get_or_create(
            staff=instance,
            start_date__lte=now,
            end_date__gte=now,
        )
        if created:
            ta = instance.percentage_work
            rt = RightTraining.objects.first()

            training.default_number_days = (rt.number_days * ta) / 100
            training.save()


@receiver(post_save, sender=Absence)
def update_training_for_staff_after_absence(sender, instance, created, raw, using, **kwargs):
    # absence
    absence = instance

    # on cree le range de cette absence
    # abs_start_date = absence.start_date
    # abs_end_date = absence.end_date
    absence_range = absence._get_range_absence()

    # on récupère que training est concerné par cette absence
    trs = Training.objects.filter(
        staff_id=instance.staff_id
    )
    if trs:
        absence_in_tr = Absence.objects.filter(
            staff_id=instance.staff_id,
            abs_type__abbr='FOR',
        )
        for tr in trs:
            # cree le total
            total_form = 0.0

            # on cree le range du tr
            tr_start_datetime = make_aware(datetime.datetime.combine(tr.start_date, datetime.time(0, 0, 0, 0)))
            tr_end_datetime = make_aware(datetime.datetime.combine(tr.end_date, datetime.time(23, 59, 59, 999999)))
            tr_range = DateTimeRange(tr_start_datetime, tr_end_datetime)
            # si l'absence est en interaction avec le tr
            if absence_range.is_intersection(tr_range):
                for abs in absence_in_tr:
                    abs_range = abs._get_range_absence()
                    if abs_range.is_intersection(tr_range):
                        for value in abs_range.range(datetime.timedelta(days=1)):
                            if tr_start_datetime <= value <= tr_end_datetime:
                                if abs.all_day:
                                    total_form += 1
                                else:
                                    total_form += 0.5

            tr.number_days = total_form
            tr.save()
