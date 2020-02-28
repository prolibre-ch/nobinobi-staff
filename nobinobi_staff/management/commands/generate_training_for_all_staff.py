import datetime
import logging

import arrow
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

from nobinobi_staff.models import RightTraining, Staff, Training


class Command(BaseCommand):
    help = _("Command for generate training for all staff.")

    def add_arguments(self, parser):
        parser.add_argument('--year', nargs='+')

    def handle(self, *args, **options):
        years = options.get("year")
        rt = RightTraining.objects.first()
        if rt:
            for year in years:
                start_date = arrow.get(datetime.date(int(year), rt.start_month, rt.start_day))
                end_date = start_date.shift(years=1, days=-1)
                staffs = Staff.objects.filter(active=True, percentage_work__isnull=False)
                for staff in staffs:
                    training, created = Training.objects.get_or_create(
                        staff=staff,
                        start_date=start_date.date(),
                        end_date=end_date.date(),
                    )
                    if created:
                        ta = staff.percentage_work
                        training.default_number_days = (rt.number_days * ta) / 100
                        training.save()
                logging.info(_("Staff training courses are created for the year {}.".format(str(year))))
                self.stdout.write(_("Staff training courses are created for the year {}.".format(str(year))))
        else:
            logging.info(_("There's no right to information training."))
            self.stdout.write(_("There's no right to information training."))

