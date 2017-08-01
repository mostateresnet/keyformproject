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
    email_requests = Request.objects.filter(locksmith_email_sent=False).select_related('building')
    buildings = Building.objects.all().prefetch_related('contact_set__alert_statuses')

    recipient_dict = {b: b.contact_set.all() for b in buildings}

    for request in email_requests:
        recipients = [c.email for c in recipient_dict[request.building]]
        subject = _('%(subject_prefix)sA request has been created') % {'subject_prefix': settings.EMAIL_SUBJECT_PREFIX}
        from_email = settings.SERVER_EMAIL

        html_content = render_to_string('keyform/emails/status_update.html',
                                        {'request': request, 'url_prefix': settings.EMAIL_URL_PREFIX})
        text_content = strip_tags(html_content)

        message = EmailMultiAlternatives(subject, text_content, from_email, recipients)
        message.attach_alternative(html_content, 'text/html')
        message.send()
        request.locksmith_email_sent = True
        request.save()


def send_update_emails():
    email_requests = Request.objects.filter(updated=False).select_related('building')
    buildings = Building.objects.all().prefetch_related('contact_set')

    recipient_dict = {b: b.contact_set.all() for b in buildings}

    for request in email_requests:
        recipients = [c.email for c in recipient_dict[request.building] if request.status in c.alert_statuses.all()]

        subject = _('%(subject_prefix)sA request has been updated from %(previous_status)s to %(status)s.') % {
            'subject_prefix': settings.EMAIL_SUBJECT_PREFIX,
            'previous_status': request.previous_status,
            'status': request.status}
        from_email = settings.SERVER_EMAIL

        html_content = render_to_string('keyform/emails/status_update.html',
                                        {'request': request, 'url_prefix': settings.EMAIL_URL_PREFIX})
        text_content = strip_tags(html_content)
        message = EmailMultiAlternatives(subject, text_content, from_email, recipients)
        message.attach_alternative(html_content, 'text/html')
        message.send()
        request.updated = True
        request.save()
