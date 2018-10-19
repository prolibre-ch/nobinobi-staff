# coding=utf-8

from django.contrib import admin
from django.contrib.admin import StackedInline
from django.utils.translation import gettext as _
from .models import Absence, Qualification, Team, Staff, AbsenceType, AbsenceAttachment


class AbsenceInline(StackedInline):
    model = Absence
    extra = 0
    verbose_name_plural = 'Absences'
    suit_classes = 'suit-tab suit-tab-absence'


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
        'last_name', 'first_name', 'qualification', 'percentage_work', 'working_time', 'preparation_time',
        'active'
    )
    list_filter = ('active', 'last_name', 'first_name')
    ordering = ('last_name',)
    inlines = (AbsenceInline,)
    search_fields = ('last_name', 'first_name')
    readonly_fields = ('working_time', 'preparation_time',)
    fieldsets = [
        (_('Staff informations'),
         {
             'classes': ('suit-tab', 'suit-tab-info',),
             'fields': ['first_name', 'last_name', 'gender', 'birthday_date', 'street', 'zip', 'city', 'phone',
                        'mobile_phone', 'email', 'avs', 'active',
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
            'fields': ['percentage_work', 'working_time', 'preparation_time']
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
    # actions = [delete_selected]
    # FIXME:A REACTIVER
    #
    # def __init__(self, model, admin_site):
    #     super(AbsenceAdmin).__init__(model, admin_site)
    #     # init variable
    #     self.end_date = None
    #     self.start_date = None
    #     self.staff = None
    #     self.abs_type = None
    #
    # def save_model(self, request, obj, form, change):
    #     """
    #     function when de absence is saved
    #     :param request:
    #     :param obj:
    #     :param form:
    #     :param change:
    #     """
    #     # create variable
    #     range_date = []
    #     range_date_anc = []
    #     range_date_absence = []
    #     self.end_date = arrow.get(form.cleaned_data['end_date'])
    #     self.start_date = arrow.get(form.cleaned_data['start_date'])
    #     self.abs_type = form.cleaned_data['abs_type']
    #     self.staff = form.cleaned_data['staff']
    #
    #     # create list with day of range
    #     for r in arrow.Arrow.range('day', self.start_date, self.end_date):
    #         range_date.append(r.date())
    #
    #     # try to get if horaire special existe
    #
    #     try:
    #         hs = DiaryPlanning.objects.filter(staff=self.staff,
    #                                           date__range=[self.start_date.date(), self.end_date.date()])
    #     except DiaryPlanning.DoesNotExist:
    #         # create the horaire special
    #         for date in range_date:
    #             self.create_horaire_special(date, self.staff)
    #     else:  # if exist
    #         for absence in hs:  # fill de list with horaire special date
    #             range_date_absence.append(absence.date)
    #
    #         if change:  # if value has changed
    #             try:
    #                 get_absence = Absence.objects.get(pk=obj.id)  # get the absence for this id
    #             except Absence.DoesNotExist:
    #                 messages.debug(request, _("Personnel admin: l'absence n'a pas pu etre récuperée."))
    #             else:
    #                 # if start_date or end_date has changed
    #                 if get_absence.end_date != form.cleaned_data['end_date'] or get_absence.start_date != \
    #                     form.cleaned_data['start_date']:
    #                     # fill the new list with absence getted
    #                     for r in arrow.Arrow.range('day', arrow.get(get_absence.start_date),
    #                                                arrow.get(get_absence.end_date)):
    #                         range_date_anc.append(r.date())
    #
    #                     # if two list is not equal
    #                     if range_date != range_date_anc:
    #                         # create new list with diff beetwen two
    #                         new_list = list(set(range_date_anc) - set(range_date))
    #                         for absence in new_list:
    #                             try:
    #                                 # try to get de horaise special with date of absence
    #                                 horaire_special = DiaryPlanning.objects.get(staff=self.staff, date=absence)
    #                             except DiaryPlanning.DoesNotExist:
    #                                 # if not exist continue
    #                                 pass
    #                             else:
    #                                 # else delete de horaire special
    #                                 horaire_special.delete()
    #
    #         # create de horaire special normaly
    #         for date in range_date:
    #             if date not in range_date_absence:
    #                 self.create_horaire_special(date, self.staff)
    #     finally:
    #         messages.success(request, _("Les horaires spéciaux ont été ajoutés."))
    #
    #     # save
    #     obj.save()
    #
    # @staticmethod
    # def create_horaire_special(date, staff):
    #     """
    #     function for create horaire special
    #     :param date:
    #     :param staff:
    #     """
    #     hs = DiaryPlanning()
    #     hs.staff = staff
    #     hs.date = date
    #     hs.absence = True
    #     hs.save()
    #
    # def delete_model(self, request, obj):
    #     """
    #     method when delete absence
    #     :param request:
    #     :param obj:
    #     """
    #     try:
    #         get_absence = Absence.objects.get(pk=obj.id)
    #     except ObjectDoesNotExist:
    #         messages.debug(request, _("Personnel admin: l'absence n'a pas pu etre récuperée."))
    #     else:
    #         try:
    #             horaire_speciaux = DiaryPlanning.objects.filter(staff=get_absence.staff,
    #                                                             date__range=[get_absence.start_date,
    #                                                                          get_absence.end_date])
    #         except DiaryPlanning.DoesNotExist:
    #             pass
    #         else:
    #             for hs in horaire_speciaux:
    #                 hs.delete()
    #     super(AbsenceAdmin, self).delete_model(request, obj)


@admin.register(AbsenceType)
class AbsenceTypeAdmin(admin.ModelAdmin):
    list_filter = ('reason',)
    ordering = ('reason',)
    search_fields = ('reason',)


@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_filter = ('name', 'short_name', 'order', 'used_ratio')
    list_display = ('name', 'short_name', 'order', 'used_ratio')
    ordering = ('order', 'name',)
    search_fields = ('name', 'short_name', 'used_ratio')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ('name',)
    readonly_fields = ("slug",)
    ordering = ('name',)
    search_fields = ('name',)
