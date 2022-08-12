from django.contrib import admin

from meetCalendar.models import meetDay,meetTravel,meetDayInfo,meetTravelInfo

# Register your models here.
@admin.register(meetDay)
class meetDayAdmin(admin.ModelAdmin):
    list_display= ('meetId', 'userId', 'startTime', 'endTime')
    pass

@admin.register(meetTravel)
class meetTravelAdmin(admin.ModelAdmin):
    list_display= ('meetId', 'userId', 'startDate', 'endDate')
    pass

@admin.register(meetDayInfo)
class meetDayInfoAdmin(admin.ModelAdmin):
    list_display= ('meetId', 'year', 'month', 'day', 'hours')
    pass

@admin.register(meetTravelInfo)
class meetTravelInfoAdmin(admin.ModelAdmin):
    list_display= ('meetId', 'year', 'month', 'day')
    pass