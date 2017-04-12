from django import forms
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.forms import TypedChoiceField
from django.forms.models import inlineformset_factory
from keyform.models import Request, KeyData
from betterforms.multiform import MultiModelForm

class CreateForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['building', 'student_name', 'reason_for_request', 'amt_recieved', 'payment_method', 'charge_amount', 'staff', 'bpn', 'charged_on_rcr']

    def __init__(self, *args, **kwargs):
        super(CreateForm, self).__init__(*args, **kwargs)
        #removes blank choices from Radio Select options
        self.fields['payment_method'] = TypedChoiceField(widget=RadioSelect(), choices=Request.PAYMENT_TYPES)
        self.fields['reason_for_request'] = TypedChoiceField(widget=RadioSelect(), choices=Request.REQUEST_TYPES)

class KeyDataForm(forms.ModelForm):
    class Meta:
        model = KeyData
        fields = ['new_core_number', 'key_type', 'room_number', 'lost_key_number', 'quantity']

RequestFormSet = inlineformset_factory(Request, KeyData, extra=1, can_delete=False, exclude=[])


class MultiFormDisplay(MultiModelForm):
    form_classes = {
        'Personal_data': CreateForm,
        'Official_data': KeyDataForm,
    }

