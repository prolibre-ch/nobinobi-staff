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
import logging

import arrow
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

from nobinobi_staff.models import RightTraining, Staff, Training


class Command(BaseCommand):
    help = _("Command for generate training.")

    def add_arguments(self, parser):
        parser.add_argument('--years', nargs='+')
        parser.add_argument('--staffs', nargs='+')

    def handle(self, *args, **options):
        staffs = options.get("staffs")
        years = options.get("years")
        # if not years write call for now year
        if not years:
            years = [timezone.localdate().year]

        if not staffs:
            staffs = Staff.objects.filter(status=Staff.STATUS.active,
                                          percentage_work__isnull=False
                                          ).values_list("id", flat=True)

        rt = RightTraining.objects.first()
        if rt:
            for year in years:
                start_date = arrow.get(datetime.date(int(year), rt.start_month, rt.start_day))
                end_date = start_date.shift(years=1, days=-1)
                for staff in staffs:
                    training, created = Training.objects.get_or_create(
                        staff_id=staff,
                        start_date=start_date.date(),
                        end_date=end_date.date(),
                    )
                    if created:
                        st = Staff.objects.get(id__exact=staff)
                        training.default_number_days = (rt.number_days * st.percentage_work) / 100
                        training.save()
                        logging.info(
                            _("Staff {0} training courses are created for the year {1}.".format(st.full_name,
                                                                                                str(year))))
                        self.stdout.write(
                            _("Staff {0} training courses are created for the year {1}.".format(st.full_name,
                                                                                                str(year))))
        else:
            logging.info(_("There's no right to information training."))
            self.stdout.write(_("There's no right to information training."))
