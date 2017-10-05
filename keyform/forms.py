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
        self.fields['payment_method'] = TypedChoiceField(widget=RadioSelect(), choices=Request.PAYMENT_TYPES, 
            help_text=_("Cash/Check should only be accepted during camps and conferences, and also fill in the amount received. Use the Charge Amount box to charge to the student's account, or mark that the student was charged on the RCR if they are checking out."))
        self.fields['reason_for_request'] = TypedChoiceField(widget=RadioSelect(), choices=Request.REQUEST_TYPES)

    def clean(self):
        cleaned_data = super(CreateForm, self).clean()
        reason_for_request = cleaned_data.get("reason_for_request")
        amt_received = cleaned_data.get("amt_received")
        payment_method = cleaned_data.get("payment_method")
        bpn = cleaned_data.get("bpn")
        student_name = cleaned_data.get("student_name")
        charge_amount = cleaned_data.get("charge_amount")
        charged_on_rcr = cleaned_data.get("charged_on_rcr")

        if reason_for_request == "lk":
            if not bpn:
                error_msg = _("Must have Bearpass Number when Lost/Stolen Key.")
                self.add_error('bpn', error_msg)

            if not student_name:
                error_msg = _("Must have Student Name when Lost/Stolen Key.")
                self.add_error('student_name', error_msg)

            if amt_received <= 0 and charge_amount <= 0 and not charged_on_rcr:
                error_msg = _("You must pick a billing method.")
                self.add_error(None, error_msg)
                error_msg = _("Choose one.")
                self.add_error('amt_received', error_msg)
                self.add_error('charge_amount', error_msg)
                self.add_error('charged_on_rcr', error_msg)

        if amt_received > 0 and payment_method == "na":
            error_msg = _("If Amount Received is greater than zero, Payment Method must be selected.")
            self.add_error('payment_method', error_msg)

        if amt_received == 0 and payment_method != "na":
            error_msg = _("If a Payment Method is selected, Amount Received cannot be zero.")
            self.add_error('amt_received', error_msg)
        return cleaned_data


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['name', 'email', 'buildings', 'alert_statuses']
        widgets = {
            'buildings': CheckboxSelectMultiple,
            'alert_statuses': CheckboxSelectMultiple,
        }


class EditForm(forms.ModelForm):

    class Meta:
        model = Request
        fields = ['status']


RequestFormSet = inlineformset_factory(Request, KeyData, extra=1, can_delete=False, exclude=[])
