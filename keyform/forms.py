from django import forms
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.forms import TypedChoiceField, ChoiceField
from django.forms.models import inlineformset_factory
from keyform.models import Request, KeyData, Contact, Building

class CreateForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['building', 'student_name', 'reason_for_request', 'amt_recieved', 'payment_method', 'charge_amount', 'staff', 'bpn', 'charged_on_rcr']

    def __init__(self, *args, **kwargs):
        super(CreateForm, self).__init__(*args, **kwargs)
        #removes blank choices from Radio Select options
        self.fields['payment_method'] = TypedChoiceField(widget=RadioSelect(), choices=Request.PAYMENT_TYPES)
        self.fields['reason_for_request'] = TypedChoiceField(widget=RadioSelect(), choices=Request.REQUEST_TYPES)

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'building']
        widgets = {
            'building': CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

class EditForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['status']

RequestFormSet = inlineformset_factory(Request, KeyData, extra=1, can_delete=False, exclude=[])
