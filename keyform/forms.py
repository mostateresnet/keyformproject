from django import forms
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.forms import TypedChoiceField
from django.forms.models import inlineformset_factory
from keyform.models import Request, KeyData, Comment

class CreateForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['building', 'student_name', 'reason_for_request', 'amt_received', 'payment_method', 'charge_amount', 'bpn', 'charged_on_rcr']

    def __init__(self, *args, **kwargs):
        super(CreateForm, self).__init__(*args, **kwargs)
        # removes blank choices from Radio Select options
        self.fields['payment_method'] = TypedChoiceField(widget=RadioSelect(), choices=Request.PAYMENT_TYPES)
        self.fields['reason_for_request'] = TypedChoiceField(widget=RadioSelect(), choices=Request.REQUEST_TYPES)

class EditForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['status']

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']

RequestFormSet = inlineformset_factory(Request, KeyData, extra=1, can_delete=False, exclude=[])
