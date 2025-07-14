from django import forms
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple, NumberInput
from django.forms import TypedChoiceField, MultiValueField, IntegerField, MultiWidget
from django.core.validators import MinValueValidator
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from keyform.models import Request, KeyData, Contact, KeyType

class ChargeAmountWidget(MultiWidget):
    template_name = 'keyform/includes/charge_amount_widget.html'

    def decompress(self, value):
        return []

class ChargeAmountField(MultiValueField):
    def __init__(self, *args, **kwargs):
        """
        Initialization function with pre-defined fields for each charge item.
        :param args: positional args passed to parent class.
        :param kwargs: keyword args passed to parent class.
        """
        core_change_field = IntegerField(
            required=False,
            initial=0,
            validators=[MinValueValidator(0)],
            label="Core Change(s)",
            help_text="If you don't need this, you can mark zero.",
        )
        core_change_field.widget.attrs = {'data-charge-amt': 50}

        room_key_field = IntegerField(
            required=False,
            initial=0,
            validators=[MinValueValidator(0)],
            label="Room Key(s)",
            help_text="If you don't need this, you can mark zero.",
        )
        room_key_field.widget.attrs = {'data-charge-amt': 10}

        mailbox_key_field = IntegerField(
            required=False,
            initial=0,
            validators=[MinValueValidator(0)],
            label="Mailbox Key(s)",
            help_text="If you don't need this, you can mark zero.",
        )
        mailbox_key_field.widget.attrs = {'data-charge-amt': 10}

        fields = (
            core_change_field,
            room_key_field,
            mailbox_key_field,
        )
        for field in fields:
            field.widget.attrs['label'] = field.label
        widgets = [field.widget for field in fields]

        super(ChargeAmountField, self).__init__(
            fields=fields, widget=ChargeAmountWidget(widgets),
            require_all_fields=True, *args, **kwargs
        )

    def compress(self, data_list):
        """
        Calculates total charge amount based on quantity and price.
        :param data_list: list of values of quantities of each item.
        :return: total_amt: total calculated charge.
        """
        field_prices = [f.widget.attrs['data-charge-amt'] for f in self.fields]
        total_amt = 0
        for price, count in zip(field_prices, data_list):
            total_amt += count * price
        return total_amt

class CreateForm(forms.ModelForm):
    billing_items = [
        (50, "Core Change = $50"),
        (10, "Room Key = $10"),
        (10, "Mailbox Key = $10"),
    ]


    charge_amount = ChargeAmountField(label='Charges')

    class Meta:
        model = Request
        fields = ['building', 'student_name', 'bpn', 'reason_for_request', 'amt_received', 'payment_method',
                  'charge_amount', 'charged_on_rcr']

    def __init__(self, *args, **kwargs):
        """
        Initialization function with validations to payment method field.
        :param args:  positional args passed to parent class.
        :param kwargs: keyword args passed to parent class.
        """
        super(CreateForm, self).__init__(*args, **kwargs)

        self.fields['payment_method'] = TypedChoiceField(widget=RadioSelect(), choices=Request.PAYMENT_TYPES,
                                                         label=_("Paid by:"),
                                                         help_text=_(
                                                             "Cash/Check should only be accepted during camps and"
                                                             "conferences, and also fill in the amount received. Use the"
                                                             "Charge Amount box to charge to the student's account, or "
                                                             "mark that the student was charged on the RCR if they are "
                                                             "checking out."))

    def clean(self):
        """
        Validates the form to ensure fields are provided based on the request type.
        :return: cleaned_data: dictionary containing the validated and cleaned data from the form fields.
        """
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

    def clean_email(self):
        """
        Cleans the email field and converts it into lowercase.
        :return: email: email address string in lowercase.
        """
        email = self.cleaned_data.get('email')
        return email.lower()


class EditForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['status']


class KeyDataForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """
        Initialization function that dynamically adds attributes to the key type field.
        :param args:  positional args passed to parent class.
        :param kwargs: keyword args passed to parent class.
        """
        super(KeyDataForm, self).__init__(*args, **kwargs)
        key_type_attrs = {
            'data-pks_with_hide_core_number': ','.join(
                [str(kt.pk) for kt in self.fields['key_type'].queryset if kt.hide_core_number]),
        }
        self.fields['key_type'].widget.attrs.update(key_type_attrs)


RequestFormSet = inlineformset_factory(Request, KeyData, form=KeyDataForm, extra=1, can_delete=False, exclude=[])
