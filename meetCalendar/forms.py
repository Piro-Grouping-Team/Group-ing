from django import forms
import datetime
from meetCalendar.models import meetDay, meetTravel

class meetDayForm(forms.ModelForm):
    class Meta:
        model = meetDay
        fields = ['validDate', 'startTime', 'endTime']
        
    validDate = forms.DateInput(format=('%m/%d/%Y'),attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'})
    startTime = forms.TimeInput(format=('%H:%M'),attrs={'class':'form-control', 'placeholder':'Select a time', 'type':'time'})
    endTime = forms.TimeInput(format=('%H:%M'),attrs={'class':'form-control', 'placeholder':'Select a time', 'type':'time'})

    def clean_endTime(self):
        startTime = self.cleaned_data['startTime']
        endTime = self.cleaned_data['endTime']

        if startTime > endTime:
            raise forms.ValidationError("Start date must be earlier than end date")
        return endTime

class meetTravelForm(forms.ModelForm):
    TIME_CHOICE = (
        ('0', '00 ~ 01'),
        ('1', '01 ~ 02'),
        ('2', '02 ~ 03'),
        ('3', '03 ~ 04'),
        ('4', '04 ~ 05'),
        ('5', '05 ~ 06'),
        ('6', '06 ~ 07'),
        ('7', '07 ~ 08'),
        ('8', '08 ~ 09'),
        ('9', '09 ~ 10'),
        ('10', '10 ~ 11'),
        ('11', '11 ~ 12'),
        ('12', '12 ~ 13'),
        ('13', '13 ~ 14'),
        ('14', '14 ~ 15'),
        ('15', '15 ~ 16'),
        ('16', '16 ~ 17'),
        ('17', '17 ~ 18'),
        ('18', '18 ~ 19'),
        ('19', '19 ~ 20'),
        ('20', '20 ~ 21'),
        ('21', '21 ~ 22'),
        ('22', '22 ~ 23'),
        ('23', '23 ~ 00'),
    )
    class Meta:
        model = meetTravel
        fields = ['startDate','endDate', 'startTime', 'endTime']
        

    startDate = forms.DateInput(format=('%m/%d/%Y'),attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'})
    endDate = forms.DateInput(format=('%m/%d/%Y'),attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'})


    def clean_endDate(self):
        startDate = self.cleaned_data['startDate']
        endDate = self.cleaned_data['endDate']

        if startDate >= endDate:
            raise forms.ValidationError("Start date must be earlier than end date")
        return endDate
    
    