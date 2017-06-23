from django.core.management.base import BaseCommand
from keyform.models import Request, Contact, Building
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        send_locksmith_emails()
        send_update_emails()


def send_locksmith_emails():
    email_requests = Request.objects.filter(locksmith_email_sent=False)
    buildings = Building.objects.all().prefetch_related('contact_set')

    recipient_dict = {b:b.contact_set.all() for b in buildings}

    for request in email_requests:
        recipients = [c.email for c in recipient_dict[request.building]]
        subject = settings.EMAIL_SUBJECT_PREFIX + _('A request has been created')
        from_email = settings.SERVER_EMAIL

        html_content = render_to_string('keyform/emails/status_update.html', {'request': request})
        text_content = strip_tags(html_content)

        message = EmailMultiAlternatives(subject, text_content, from_email, recipients)
        message.attach_alternative(html_content, 'text/html')
        message.send()
        print("Sent an email to", recipients)
        request.locksmith_email_sent = True
        request.save()

def send_update_emails():
    email_requests = Request.objects.filter(updated=False).select_related('building')
    buildings = Building.objects.all().prefetch_related('contact_set')

    recipient_dict = {b:b.contact_set.all() for b in buildings}

    for request in email_requests:
        recipients = [c.email for c in recipient_dict[request.building]]
        subject = settings.EMAIL_SUBJECT_PREFIX + _('A request has been updated from %(previous_status)s to %(status)s.') % {'previous_status': request.get_previous_status_display(), 'status': request.get_status_display()}
        from_email = settings.SERVER_EMAIL

        html_content = render_to_string('keyform/emails/status_update.html', {'request': request})
        text_content = strip_tags(html_content)

        message = EmailMultiAlternatives(subject, text_content, from_email, recipients)
        message.attach_alternative(html_content, 'text/html')
        message.send()
        request.updated = True
        request.save()
