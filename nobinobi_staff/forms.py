import arrow
from datetimerange import DateTimeRange
from django.forms import ModelForm, forms
from django.utils import timezone
from django.utils.translation import gettext as _
from nobinobi_staff.models import Absence


class AbsenceAdminForm(ModelForm):
    """ Formulaire pour le admin absence"""

    class Meta:
        model = Absence
        fields = '__all__'

        """Constructor for AbsenceAdminForm"""

    def clean(self):
        cleaned_data = super().clean()
        # get value
        staff = cleaned_data.get('staff')
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        # create a range from form
        form_absence_range = DateTimeRange(start_date, end_date)
        # get absences
        absences = Absence.objects.filter(
            start_date__lte=end_date,
            end_date__gte=start_date,
            staff_id=staff.id
        )
        for absence in absences:
            # create a range absence
            absence_range = DateTimeRange(absence.start_date, absence.end_date)
            # if form range is intersection with absence range raise error
            if form_absence_range.is_intersection(absence_range):
                raise forms.ValidationError(_('An absence already exists on these dates.'), code='invalid')
        return cleaned_data

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
