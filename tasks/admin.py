from django.contrib import admin

from tasks.models import Task


@admin.register(Task)
class UserTask(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('id', 'worker', 'customer', 'title', 'status')
    fieldsets = (
        (None, {'fields': (
            'worker', 'customer', 'status', 'title', 'description', 'report', 'closed_at'
        )}),
    )

    ordering = ('id',)

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False
