from django.contrib import admin
from .models import Meetings


# Register your models here.
@admin.register(Meetings)
class MeetingsAdmin(admin.ModelAdmin):
    list_display = ('meetName','meetPlace', 'meetStatus')