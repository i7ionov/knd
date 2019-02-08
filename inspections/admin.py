from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin

from dictionaries.models import Document
from .models import ControlKind, ControlForm, InspectionSubject, InspectionTask, LegalBasis, Inspection, \
    InspectionResult, PreceptStatus, PreceptResult, ViolationType, Cancellation, Precept


class ViolationAdmin(DjangoMpttAdmin):
    pass


class DocumentAdmin(admin.ModelAdmin):
    list_filter = ('doc_type',)
    search_fields = ('id',)
    fields = ('doc_number', 'doc_date', 'doc_type')


admin.site.register(ControlKind)
admin.site.register(ControlForm)
admin.site.register(InspectionSubject)
admin.site.register(InspectionTask)
admin.site.register(LegalBasis)
admin.site.register(Cancellation)
admin.site.register(InspectionResult)
admin.site.register(PreceptStatus)
admin.site.register(PreceptResult)
admin.site.register(ViolationType, ViolationAdmin)
admin.site.register(Document, DocumentAdmin)
