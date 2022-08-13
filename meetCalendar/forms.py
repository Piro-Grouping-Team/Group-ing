from django import forms

from meetCalendar.models import meetDay


class meetDayForm(forms.ModelForm):
    class Meta:
        model = meetDay
        fields = ['validDate', 'startTime', 'endTime']