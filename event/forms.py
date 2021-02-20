from django.forms import ModelForm, DateInput
from .models import Event
from django import forms


class EventForm(ModelForm):
    date = forms.DateTimeField(
        label="Date",
        widget=forms.DateInput(format=("%d-%m-%Y"), attrs={"type": "date",},),
    )
    start_time = forms.TimeField(
        label="Heure de début",
        widget=forms.DateInput(format=("%d-%m-%Y"), attrs={"type": "time",},),
    )
    end_time = forms.TimeField(
        label="Heure de fin",
        widget=forms.DateInput(format=("%d-%m-%Y"), attrs={"type": "time",},),
    )

    class Meta:
        model = Event
        # datetime-local is a HTML5 input type, format to make date time show on fields
        fields = ("name", "slot")


class AddEventMemberForm(forms.Form):
    user = forms.CharField(
        widget=forms.TextInput(attrs={"value": "", "type": "hidden"}),
    )
    event = forms.CharField(
        widget=forms.TextInput(attrs={"value": "", "type": "hidden"}),
    )
