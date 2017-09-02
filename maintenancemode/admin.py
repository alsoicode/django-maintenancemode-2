from django.contrib import admin

from maintenancemode.models import Maintenance, IgnoredURL


class IgnoredURLInline(admin.TabularInline):
    model = IgnoredURL
    extra = 3


class MaintenanceAdmin(admin.ModelAdmin):
    inlines = [IgnoredURLInline, ]
    list_display = ['__str__', 'is_being_performed']
    readonly_fields = ('site',)
    actions = None

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


admin.site.register(Maintenance, MaintenanceAdmin)
