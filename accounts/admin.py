from django.contrib import admin

from accounts.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'role')
    list_display = ('id', 'email', 'username', 'phone', 'role')
    fieldsets = (
        (None, {'fields': (
            'username', 'email', 'first_name', 'last_name', 'patronymic', 'role', 'phone',
        )}),
        ('Permissions', {'fields': ('is_can_create_tasks', 'is_have_access_to_tasks', 'is_can_add_customers',
                                    'is_can_add_workers', 'is_have_access_to_workers'
                                    )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'first_name', 'last_name', 'patronymic', 'role', 'phone',
            )}
         ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)
