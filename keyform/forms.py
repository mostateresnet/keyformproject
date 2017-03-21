from django import forms
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.forms import TypedChoiceField
from keyform.models import Request

class CreateForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['building', 'student_name', 'reason_for_request', 'amt_recieved', 'payment_method', 'charge_amount', 'staff', 'bpn', 'created_timestamp', 'charged_on_rcr']


    def clean(self):
        cleaned_data = super(CreateForm, self).clean()

    def __init__(self, *args, **kwargs):
        super(CreateForm, self).__init__(*args, **kwargs)
        self.fields['payment_method'] = TypedChoiceField(widget=RadioSelect(), choices=Request.PAYMENT_TYPES)
        self.fields['reason_for_request'] = TypedChoiceField(widget=RadioSelect(), choices=Request.REQUEST_TYPES)
