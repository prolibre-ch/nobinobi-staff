from datetime import datetime

import arrow
from datetimerange import DateTimeRange
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.timezone import make_aware

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
    trs = None
    try:
        trs = list(Training.objects.get(
            start_date__lte=instance.end_date,
            end_date__gte=instance.start_date,
            staff_id=instance.staff_id
        ))
    except Training.DoesNotExist:
        pass
    except Training.MultipleObjectsReturned:
        trs = Training.objects.filter(
            start_date__lte=instance.end_date,
            end_date__gte=instance.start_date,
            staff_id=instance.staff_id
        )

    absences_list = []
    for tr in trs:
        absences = Absence.objects.filter(
            staff_id=instance.staff.id,
            start_date__lte=tr.end_date,
            end_date__gte=tr.start_date,
            abs_type__abbr='FOR').order_by('start_date')

        total_form = 0.0
        for abs in absences:
            datetime_absence_range = DateTimeRange(abs.start_date, abs.end_date)
            for value in datetime_absence_range.range(datetime.timedelta(days=1)):
                for day in value:
                    if abs.all_day:
                        total_form += 1
                    else:
                        total_form += 0.5

            print(total_form)
    # start_date = instance.start_
    # end_date = None
    # +1 for accept 12 in range
    # start_datetime = datetime.combine(start_date, 0, 0, 0, 0)
    # end_date = datetime.combine(end_date, 23, 59, 59, 99999)
