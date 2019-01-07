# coding=utf-8
import arrow
from django.contrib import admin
from django.contrib.admin import StackedInline
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.forms import BaseInlineFormSet
from django.utils.translation import gettext as _
from nobinobi_core.functions import AdminInlineWithSelectRelated

from .models import Absence, Qualification, Team, Staff, AbsenceType, AbsenceAttachment


class InlineAbsenceFormset(BaseInlineFormSet):
    def clean(self):
        super(InlineAbsenceFormset, self).clean()
        errors = []
        for form in self.forms:
            try:
                form.cleaned_data['start_date']
            except KeyError:
                form.cleaned_data["start_date"] = arrow.now().datetime
            else:
                if form.cleaned_data["start_date"] > form.cleaned_data["end_date"]:
                    msg = _("The start date is greater than the end date.")
                    errors.append(msg)
                    form._errors[NON_FIELD_ERRORS] = self.error_class([msg])

        if errors:
            raise ValidationError(errors)


class AbsenceInline(AdminInlineWithSelectRelated, StackedInline):
    model = Absence
    extra = 0
    verbose_name_plural = 'Absences'
    suit_classes = 'suit-tab suit-tab-absences'
    # raw_id_fields = ("abs_type",)
    suit_form_inlines_hide_original = True
    list_select_related = [
        "abs_type",
        "staff",
    ]
    formset = InlineAbsenceFormset  # line to add


class AbsenceAttachmentInline(StackedInline):
    model = AbsenceAttachment
    extra = 0
    verbose_name_plural = 'AbsencesAttachment'
    suit_classes = 'suit-tab suit-tab-file'


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    # on garde les filtres actif en enregistrant
    preserve_filters = True

    suit_form_tabs = (('info', _('Staff informations')), ('absences', _('Absences')),)
    list_display = (
        'last_name', 'first_name', 'qualification', 'percentage_work', 'working_time', 'active'
    )
    list_filter = ('active', 'last_name', 'first_name')
    ordering = ('last_name',)
    inlines = (AbsenceInline,)
    search_fields = ('last_name', 'first_name')
    readonly_fields = ('working_time',)
    fieldsets = [
        (_('Staff informations'),
         {
             'classes': ('suit-tab', 'suit-tab-info',),
             'fields': ['first_name', 'last_name', 'gender', 'birth_date', 'street', 'zip', 'city', 'phone',
                        'mobile_phone', 'email', 'avs', 'active', 'team',
                        'user']
         }),
        (_('Qualification'),
         {
             'classes': ('suit-tab', 'suit-tab-info',),
             'fields': ['qualification', ]
         }),
        (_('Date'), {
            'classes': ('suit-tab', 'suit-tab-info',),
            'fields': ['arrival_date', 'departure_date']
        }),
        (_('Planning'), {
            'classes': ('suit-tab', 'suit-tab-info',),
            'description': _("Occupancy rate (based on a 40-hour weekly schedule)"),
            'fields': ['percentage_work', 'working_time']
        }), ]

    # TODO:VOIR POUR SI NECCESAIRE
    # actions = ['act_dact_staff']
    #
    # def act_dact_staff(self, request, queryset):
    #     rows_updated = 0
    #     for q in queryset:
    #         # pour chaque selectionne
    #         if q.actif:
    #             # si il est actif
    #             q.actif = False
    #             # on le desactive et on rentre les dates
    #             q.date_reactivation = None
    #             q.date_desactivation = arrow.utcnow().format('YYYY-MM-DD')
    #         # si pas actif on le met actif
    #         else:
    #             q.actif = True
    #             # on rentre les dates
    #             q.date_desactivation = None
    #             q.date_reactivation = arrow.utcnow().format('YYYY-MM-DD')
    #         # on sauve
    #         q.save()
    #         rows_updated += 1
    #
    #     if rows_updated == 1:
    #         message_bit = _("1 personne a été activé/désactivé.")
    #     else:
    #         message_bit = _("{0} personnes ont étés activés/désactivés.").format(rows_updated)
    #     messages.success(request, "%s" % message_bit)
    #
    # act_dact_staff.short_description = _("Activer/désactiver une(des) personne(s)")

    def get_formsets(self, request, obj=None):
        """
        Set extra=0 for inlines if object already exists
        """
        for inline in self.get_inline_instances(request):
            formset = inline.get_formset(request, obj)
            if obj:
                formset.extra = 0
            yield formset


@admin.register(Absence)
class AbsenceAdmin(admin.ModelAdmin):
    suit_form_tabs = (('info', _('Absence informations')), ('file', _('Files')),)
    inlines = (AbsenceAttachmentInline,)
    list_filter = ('abs_type', 'start_date', 'end_date')
    list_display = ('staff', 'abs_type', 'start_date', 'end_date')
    ordering = ('-start_date',)
    search_fields = ('staff__last_name', 'staff__first_name')
    fieldsets = [
        (_('Information'),
         {
             'classes': ('suit-tab', 'suit-tab-info',),
             'fields': ['staff', 'abs_type'],
         }),
        (_('Date'),
         {
             'classes': ('suit-tab', 'suit-tab-info',),
             'fields': ['start_date', 'end_date', 'all_day'],
         }),
        (_('Comment'),
         {
             'classes': ('suit-tab', 'suit-tab-info',),
             'fields': ['comment'],
         }),
    ]


@admin.register(AbsenceType)
class AbsenceTypeAdmin(admin.ModelAdmin):
    list_filter = ('reason', 'abbr',)
    ordering = ('reason',)
    search_fields = ('reason', 'abbr',)


@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_filter = ('name', 'short_name', 'order',)
    list_display = ('name', 'short_name', 'order',)
    ordering = ('order', 'name',)
    search_fields = ('name', 'short_name',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    list_filter = ('name', 'order')
    readonly_fields = ("slug",)
    ordering = ('order', 'name',)
    search_fields = ('name',)
