# coding=utf-8
import datetime
import os
import uuid

import arrow
from datetimerange import DateTimeRange
from django.contrib.auth.models import User
from django.db import models
from django.db.models.functions import Upper
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import make_aware
from django.utils.translation import gettext as _
from django_auto_one_to_one import AutoOneToOneModel
from model_utils import Choices
from model_utils.models import StatusField, TimeStampedModel

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
    birth_date = models.DateField(verbose_name=_("Birth Date"), blank=True, null=True)
    street = models.CharField(_('Street'), max_length=255, null=True, blank=True)
    zip = models.PositiveIntegerField(_('ZIP'), null=True, blank=True)
    city = models.CharField(_('City'), max_length=50, null=True, blank=True)
    phone = models.CharField(_('Phone'), max_length=50, null=True, blank=True)
    mobile_phone = models.CharField(_('Mobile phone'), max_length=50, null=True, blank=True)
    avs = models.CharField(_('AVS'), max_length=16, null=True, blank=True)
    email = models.EmailField(_('Email'), null=True, blank=True)
    team = models.ForeignKey(
        to="Team",
        verbose_name=_('Team'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    qualification = models.ForeignKey(
        'Qualification',
        verbose_name=_("Qualification"),
        on_delete=models.SET_NULL,
        blank=False,
        null=True
    )
    percentage_work = models.FloatField(verbose_name=_("Percentage of work"), default=0)
    working_time = models.FloatField(_("Working time"))
    working_base = models.FloatField(verbose_name=_("Working base"), default=40)

    # recorded_time = models.FloatField(_("Temps enregistré"), default=0)
    # temps_prep_enregistre = models.FloatField(_("Temps de préparation enregistré"), default=0)
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

    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def __str__(self):  # __unicode__ on Python 2
        # Returns the person's full name.
        return '%s %s' % (self.first_name, self.last_name)  #

    def save(self, *args, **kwargs):
        self.last_name = self.last_name.title()
        self.first_name = self.first_name.title()
        percentage = self.percentage_work
        # qualification = self.qualification_id
        # on check si le percentage est entre 0 et 100
        if percentage <= 100 or percentage > 0:
            # on init les valeurs constantes
            base_work = self.working_base
            # on defini le travail
            work = (percentage / 100) * base_work
            self.working_time = work

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
    start_date = models.DateTimeField(_("Start date"))
    end_date = models.DateTimeField(_("End date"))
    all_day = models.BooleanField(_("All day"), default=False)
    comment = models.TextField(_("Comment"), blank=True, null=True)
    partial_disability = models.IntegerField(_("Partial disability"), blank=True, null=True, help_text=_("In percentage %"))

    def __str__(self):  # __unicode__ on Python 2
        return '%s | %s | %s - %s' % (
            self.staff, self.abs_type, arrow.get(self.start_date).format("DD-MM-YYYY"),
            arrow.get(self.end_date).format("DD-MM-YYYY"))

    def _get_range_absence(self):
        return DateTimeRange(self.start_date, self.end_date)

    range_absence = property(_get_range_absence)


class AbsenceType(models.Model):
    reason = models.CharField(_("Reason"), max_length=255)
    abbr = models.CharField(_("Abbreviation"), max_length=3, default="000")

    class Meta:
        verbose_name = _("Absence type")
        verbose_name_plural = _("Absences type")

    def __str__(self):  # __unicode__ on Python 2
        return "{} - {}".format(self.abbr, self.reason)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # save abbreviation in CAPITAL
        if self.abbr:
            Upper(self.abbr)
        return super(AbsenceType, self).save()


class Team(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=100)
    slug = models.SlugField(verbose_name=_("Slug"), max_length=150, unique=True)
    order = models.PositiveIntegerField(verbose_name=_("Order"), unique=True, blank=False, null=True)

    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")

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


class AbsenceAttachment(models.Model):
    ATTACHMENT_TYPE = Choices(
        ("medical", _("Medical certificate")),
        ("work", _("Work Certificate")),
    )

    def generate_new_filename(self, filename):
        f, ext = os.path.splitext(filename)
        upload_to = "staff/{}/absence/".format(self.absence.staff.racc)
        return '{}{}{}'.format(upload_to, uuid.uuid4().hex, ext)

    type = StatusField(_("Type"), choices_name="ATTACHMENT_TYPE")
    file = models.FileField(_("File"), upload_to=generate_new_filename, blank=True, null=True)
    absence = models.ForeignKey(
        verbose_name=_("Absence"),
        to="Absence",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Absence attachment")
        verbose_name_plural = _("Absence attachments")

    def __str__(self):
        return "".format(self.absence, self.file)


class RightTraining(models.Model):
    """Model to store variable for right to training"""
    MONTH_CHOICES = Choices(
        (1, _("January")),
        (2, _("February")),
        (3, _("Mars")),
        (4, _("April")),
        (5, _("May")),
        (6, _("June")),
        (7, _("July")),
        (8, _("August")),
        (9, _("September")),
        (10, _("October")),
        (11, _("November")),
        (12, _("December")),
    )

    number_days = models.IntegerField(_("Number of days"), help_text=_(
        "Number of days of training entitlement based on a 100% activity rate."))
    start_day = models.IntegerField(_("Start day"), choices=((x, x) for x in range(0, 32, 1)))
    start_month = models.IntegerField(_("Start month"), choices=MONTH_CHOICES)

    class Meta:
        # ordering = ('date',)
        verbose_name = _('Right to training')
        # verbose_name_plural = _('')

    def __str__(self):
        return str(self.number_days)


class Training(TimeStampedModel):
    """Models to store for a staff number exactly have"""
    default_number_days = models.FloatField(_("Number of days"), default=0.0)
    number_days = models.FloatField(_("Number of days"), default=0.0)
    start_date = models.DateField(_("Start date"), editable=False)
    end_date = models.DateField(_("End date"), editable=False)
    staff = models.ForeignKey(
        to=Staff,
        on_delete=models.CASCADE,
        verbose_name=_("Staff"),
        editable=False
    )

    class Meta:
        ordering = ('start_date', 'end_date',)
        verbose_name = _('Training')
        unique_together = ('start_date', 'end_date', 'staff')
        # verbose_name_plural = _('')

    def __str__(self):
        return "{} - {} - {}".format(self.staff.full_name, self.default_number_days, self.number_days)
