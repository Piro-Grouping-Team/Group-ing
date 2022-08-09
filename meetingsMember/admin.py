from django.contrib import admin
from .models import MeetingMember

# Register your models here.
@admin.register(MeetingMember)
class MeetingMemberAdmin(admin.ModelAdmin):
    pass    