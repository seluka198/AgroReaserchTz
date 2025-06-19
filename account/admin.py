from django.contrib import admin
from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'phone_number', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'phone_number')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()




