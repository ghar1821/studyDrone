from django.contrib import admin
from reporting.models import MaliciousReport


class MaliciousReportAdmin(admin.ModelAdmin):
	list_display = ('reported_by','note','report_content','submission_time')

admin.site.register(MaliciousReport,MaliciousReportAdmin)
