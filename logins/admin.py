from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from logins.models import User

class UserAdmin(UserAdmin):

    list_display = (
        'id',
        'email',
        'name',
        'is_staff',
    )
    search_fields = (
        'email',
        'name',
        'username',
    )
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User, UserAdmin)   