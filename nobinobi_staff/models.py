# coding=utf-8
import uuid

import arrow
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext as _

from model_utils import Choices

GENDER_CHOICE = Choices(
    (0, "man", _('Man')),
    (1, "woman", _('Woman')),
    (2, "other", _('Other'))
)


# Create your models here.
class Staff(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        null=True,
        blank=True,
    )
    last_name = models.CharField(_("Last name"), max_length=255)
    first_name = models.CharField(_("First name"), max_length=255)
    gender = models.SmallIntegerField(choices=GENDER_CHOICE, verbose_name=_("Gender"), blank=False, null=True)
    birthday_date = models.DateField(verbose_name=_("Birthday Date"), blank=True, null=True)
    street = models.CharField(_('Street'), max_length=255, null=True, blank=True)
    zip = models.PositiveIntegerField(_('ZIP'), null=True, blank=True)
    city = models.CharField(_('City'), max_length=50, null=True, blank=True)
    phone = models.CharField(_('Phone'), max_length=50, null=True, blank=True)
    mobile_phone = models.CharField(_('Mobile phone'), max_length=50, null=True, blank=True)
    avs = models.CharField(_('AVS'), max_length=16, null=True, blank=True)
    email = models.EmailField(_('Email'), null=True, blank=True)

    qualification = models.ForeignKey(
        'Qualification',
        verbose_name=_("Qualification"),
        on_delete=models.SET_NULL,
        blank=False,
        null=True
    )
    percentage_work = models.FloatField(verbose_name=_("Percentage of work"), default=0)
    working_time = models.FloatField(_("Working time"))
    preparation_time = models.FloatField(_("Preparation time"), default=0)
    # recorded_time = models.FloatField(_("Temps enregistré"), default=0)
    # temps_prep_enregistre = models.FloatField(_("Temps de préparation enregistré"), default=0)
    # absence = models.BooleanField(_("Absence"), default=False)
    # remplacant = models.BooleanField(verbose_name=_("Remplaçant"), default=False)
    active = models.BooleanField(verbose_name=_("Active"), default=True)
    arrival_date = models.DateField(_("Arrival date"), null=True)
    departure_date = models.DateField(_("Departure Date"), null=True, blank=True)
    # date_desactivation = models.DateField(_("Date de désactivation"), null=True, blank=True)
    # date_reactivation = models.DateField(_("Date de réactivation"), null=True, blank=True)
    # heure_sup = models.FloatField(_("Heure supplémentaire"), default=0)
    # base_classroom = models.ForeignKey(
    #     Classroom,
    #     verbose_name=_("Salle de classe"),
    #     on_delete=models.SET_NULL,
    #     blank=True,
    #     null=True
    # )

    def _get_racc_name(self):
        return '%s%s' % (slugify(str.lower(self.first_name[:2])), slugify(str.lower(self.last_name[:1])))

    racc = property(_get_racc_name)

    def get_full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def __str__(self):  # __unicode__ on Python 2
        # Returns the person's full name.
        return '%s %s' % (self.first_name, self.last_name)  #

    def save(self, *args, **kwargs):
        self.last_name = self.last_name.title()
        self.first_name = self.first_name.title()
        percentage = self.percentage_work
        qualification = self.qualification_id
        # on check si le percentage est entre 0 et 100
        if percentage <= 100 or percentage > 0:
            # on init les valeurs constantes
            base_work = 40
            preparation_times = 0
            # on defini le travail
            work = (percentage / 100) * base_work
            # on check si categorie = 1:Educatrice diplome, 2: ASE, 3. Auxiliaire
            if qualification in [1, 2, 3]:
                # on set le temps de preparation
                #  codage pour un arrondisement au 0.25 pres
                preparation_times = round(4 * (work * (10 / 100))) / 4
                # et on reedite le travail
                work -= preparation_times

            self.working_time = work
            self.preparation_time = preparation_times

        super(Staff, self).save(*args, **kwargs)

    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name_plural = _("Staffes")
        verbose_name = _("Staff")
        permissions = (("can_read_list", "Can read list"),)


class Qualification(models.Model):
    name = models.TextField(_("Name"))
    short_name = models.CharField(_("Short name"), max_length=255)
    order = models.IntegerField(_("Order"), default=1)
    used_ratio = models.BooleanField(_("Used by the ratio"), default=False)

    class Meta:
        ordering = ('order',)

    def __str__(self):  # __unicode__ on Python 2
        return self.name


class Absence(models.Model):
    staff = models.ForeignKey(
        Staff,
        verbose_name=_("Staff"),
        related_name="staff",
        on_delete=models.CASCADE
    )
    abs_type = models.ForeignKey(
        "AbsenceType",
        verbose_name=_("Absence type"),
        on_delete=models.SET_NULL,
        blank=False,
        null=True
    )
    start_date = models.DateField(_("Start date"))
    end_date = models.DateField(_("End date"))

    def __str__(self):  # __unicode__ on Python 2
        return '%s %s | %s | %s - %s' % (
            self.staff.first_name, self.staff.last_name, self.abs_type, arrow.get(self.start_date).format("DD-MM-YYYY"),
            arrow.get(self.end_date).format("DD-MM-YYYY"))

    def _get_range_absence(self):
        return [r for r in arrow.Arrow.span_range('day', arrow.get(self.start_date), arrow.get(self.end_date))]

    range_absence = property(_get_range_absence)

    def save(self, *args, **kwargs):
        """What to do when we modify or create"""
        super(Absence, self).save(*args, **kwargs)
        #FIXME: a remettre

        # if settings.ENABLE_POINTAGE:
        #     today = arrow.utcnow().date()
        #     if today > self.date_fin:
        #         from nobinobi.pointage.models import update_all_statistics_on_day
        #         for day in arrow.Arrow.range(
        #             'day',
        #             arrow.get(self.date_debut),
        #             arrow.get(self.date_fin)
        #         ):
        #             update_all_statistics_on_day(
        #                 day=day.datetime,
        #                 staff=self.staff,
        #             )
        # return to_return

    def delete(self, *args, **kwargs):
        """Delete the model"""
        super(Absence, self).delete(*args, **kwargs)
        #FIXME: a remettre
        # if settings.ENABLE_POINTAGE:
        #
        #     today = arrow.utcnow().date()
        #     if today > self.date_fin:
        #         from nobinobi.pointage.models import update_all_statistics_on_day
        #         for day in arrow.Arrow.range(
        #             'day',
        #             arrow.get(self.date_debut),
        #             arrow.get(self.date_fin)
        #         ):
        #             update_all_statistics_on_day(
        #                 day=day.datetime,
        #                 staff=self.staff,
        #             )
        # return to_return


class AbsenceType(models.Model):
    reason = models.CharField(_("Reason"), max_length=255)

    def __str__(self):  # __unicode__ on Python 2
        return self.reason

    class Meta:
        verbose_name = _("Absence type")
        verbose_name_plural = _("Absences type")


class Team(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=100)
    slug = models.SlugField(verbose_name=_("Slug"), max_length=150, unique=True)

    def __str__(self):
        return self.name

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Team.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super(Team, self).save(*args, **kwargs)
