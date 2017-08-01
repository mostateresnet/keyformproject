from django import forms
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.forms import TypedChoiceField
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from keyform.models import Request, KeyData, Contact


class CreateForm(forms.ModelForm):

    class Meta:
        model = Request
        fields = ['building', 'student_name', 'bpn', 'reason_for_request', 'amt_received', 'payment_method', 'charge_amount', 'charged_on_rcr']

    def __init__(self, *args, **kwargs):
        super(CreateForm, self).__init__(*args, **kwargs)
        # removes blank choices from Radio Select options
        self.fields['payment_method'] = TypedChoiceField(widget=RadioSelect(), choices=Request.PAYMENT_TYPES)
        self.fields['reason_for_request'] = TypedChoiceField(widget=RadioSelect(), choices=Request.REQUEST_TYPES)


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['name', 'email', 'buildings', 'alert_statuses']
        widgets = {
            'building': CheckboxSelectMultiple,
            'alert_statuses': CheckboxSelectMultiple,
        }


class EditForm(forms.ModelForm):

    class Meta:
        model = Request
        fields = ['status']


RequestFormSet = inlineformset_factory(Request, KeyData, extra=1, can_delete=False, exclude=[])
