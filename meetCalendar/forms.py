from django import forms

from meetCalendar.models import meetDay


class meetDayForm(forms.ModelForm):
    class Meta:
        model = meetDay
        fields = ['validDate', 'startTime', 'endTime']
        widgets = {
            'validDate' : forms.DateInput(format=('%m/%d/%Y'),attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
    
        }