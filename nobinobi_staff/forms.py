import arrow
from django.forms import ModelForm

from nobinobi_staff.models import Absence


class AbsenceAdminForm(ModelForm):
    """ Formulaire pour le admin absence"""

    class Meta:
        model = Absence
        fields = '__all__'

        """Constructor for AbsenceAdminForm"""

    # def clean(self):
    #     cleaned_data = super().clean()
    #     all_day = cleaned_data['all_day']
    #     start_date = self.data.get("start_date_0")
    #     start_date_time = self.data.get("start_date_time_1")
    #     end_date = self.data.get("end_date_0")
    #     end_date_time = self.data.get("end_date_1")
    #     now = arrow.now()
    #     if not start_date:
    #         start_date = now.date()
    #     if not start_date_time:
    #         if all_day:
    #             self.data.get("start_date_time_1") = now.replace(hour=6, minute=0)
    #     if not end_date:
    #         end_date = now.date()
    #     if not end_date_time:
    #         end_date_time = now.time()
    #
    #     return cleaned_data

    def __init__(self, *args, **kwargs):
        try:
            kwargs['instance']
        except KeyError:
            # on set le initial sur les dates
            try:
                kwargs['initial']
            except KeyError:
                kwargs['initial'] = {}
            finally:
                kwargs['initial']['all_day'] = True
                kwargs['initial']['start_date'] = arrow.now().replace(hour=6, minute=0, second=0)
                kwargs['initial']['end_date'] = arrow.now().replace(hour=20, minute=0, second=0)
        else:
            pass
        super(AbsenceAdminForm, self).__init__(*args, **kwargs)
