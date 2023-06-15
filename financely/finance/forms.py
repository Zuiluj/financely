from django import forms

from finance.models import BankAccount, Record, RecordType


class DateInput(forms.DateInput):
    input_type = 'date'


class DateRangeForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.widgets.DateInput(attrs={'type': 'date'}))


class AccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['name', 'type']


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['name', 'spend', 'income', 'type', 'note', 'date']
        widgets = {
            'date': DateInput(),
        }


class RecordTypeForm(forms.ModelForm):
    class Meta:
        model = RecordType
        fields = ['name', 'color']
