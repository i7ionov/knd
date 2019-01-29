from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from .models import ControlKind, ControlForm, InspectionSubject, InspectionTask, LegalBasis, Inspection, InspectionResult, PreceptStatus, PreceptResult, ViolationType, Cancellation


class ViolationAdmin(DjangoMpttAdmin):
    pass


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

