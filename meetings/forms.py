from django import forms

from .models import Meetings

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meetings
        fields = ['meetName','meetPlace','meetStart','meetEnd','meetPurpose']
        #meetType 추가필요

    meetName = forms.CharField(error_messages = {
    'required': '약속 이름을 입력해 주세요'
},max_length=100)
    meetPlace = forms.CharField(error_messages = {
    'required': '장소를 입력해 주세요'
},max_length=100)
    meetStart = forms.DateInput(format=('%m/%d/%Y'),attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'})
    meetEnd = forms.DateInput(format=('%m/%d/%Y'),attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'})
    meetPurpose = forms.CharField(error_messages = {
    'required': '목적을 입력해 주세요'
},max_length=100)
    #meetType = forms.CharField(max_length=20)

    def clean_meetEnd(self):
        meetStart = self.cleaned_data.get('meetStart')
        meetEnd = self.cleaned_data.get('meetEnd')

        if meetStart > meetEnd:
            raise forms.ValidationError('종료일은 시작일보다 빠를 수 없습니다.')
        return meetEnd




class MeetingUpdateForm(forms.ModelForm):
    class Meta:
        model = Meetings
        fields = ['meetName','meetPlace','meetPurpose']
        #meetType 추가필요

    meetName = forms.CharField(error_messages = {
    'required': '약속 이름을 입력해 주세요'
},max_length=100)
    meetPlace = forms.CharField(error_messages = {
    'required': '장소를 입력해 주세요'
},max_length=100)
    meetPurpose = forms.CharField(error_messages = {
    'required': '목적을 입력해 주세요'
},max_length=100)
    #meetType = forms.CharField(max_length=20)



