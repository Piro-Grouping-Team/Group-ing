from django.contrib import admin

from meetCalendar.models import meetDay,meetTravel,meetDayInfo,meetTravelInfo,meetDayVote,meetTravelVote

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
    list_display= ('meetId', 'year', 'month', 'day', 'hour')
    pass

@admin.register(meetTravelInfo)
class meetTravelInfoAdmin(admin.ModelAdmin):
    list_display= ('meetId', 'year', 'month', 'day')
    pass

@admin.register(meetDayVote)
class meetDayVoteAdmin(admin.ModelAdmin):
    list_display = ('meetId', 'year', 'month', 'day', 'startTime', 'endTime', 'voteUser')
    pass