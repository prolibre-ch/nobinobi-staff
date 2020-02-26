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
    trs = Training.objects.filter(
        staff_id=instance.staff_id
    )

    absences_list = []
    for tr in trs:
        tr_startdatetime = make_aware(datetime.datetime.combine(tr.start_date, datetime.time(0, 0, 0, 0)))
        tr_enddatetime = make_aware(datetime.datetime.combine(tr.end_date, datetime.time(23, 59, 59, 999999)))
        absences = Absence.objects.filter(
            staff_id=instance.staff.id,
            start_date__lte=tr.end_date,
            end_date__gte=tr.start_date,
            abs_type__abbr='FOR').order_by('start_date')

        total_form = 0.0
        for abs in absences:
            start_date = make_naive(abs.start_date)
            end_date = make_naive(abs.end_date)
            datetime_absence_range = DateTimeRange(make_aware(start_date), make_aware(end_date))
            for value in datetime_absence_range.range(datetime.timedelta(days=1)):
                if tr_startdatetime <= value <= tr_enddatetime:
                    if abs.all_day:
                        total_form += 1
                    else:
                        total_form += 0.5

            print(total_form)
        tr.number_days = total_form
        tr.save()
    # start_date = instance.start_
    # end_date = None
    # +1 for accept 12 in range
    # start_datetime = datetime.combine(start_date, 0, 0, 0, 0)
    # end_date = datetime.combine(end_date, 23, 59, 59, 99999)
