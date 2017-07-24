import sqlite3
from datetime import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.timezone import make_aware, utc
from keyform.models import *


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            c = sqlite3.connect('/tmp/keyform.db').cursor()

            buildings = {}
            for row in c.execute('select building_id, building_name from building'):
                buildings[str(row[0])] = Building.objects.get_or_create(name=row[1])[0]

            statuses = {
                '1': Status.objects.get_or_create(name='Processing', order=1)[0],
                '2': Status.objects.get_or_create(name='Key Sent', order=2)[0],
                '3': Status.objects.get_or_create(name='Key Distributed', order=3)[0],
            }
            reasons = {'1': 'dk', '2': 'lk', '3': 'sk'}
            payment_methods = {'1': None, '2': 'ca', '3': 'ch'}
            key_types = {'1': 'rm', '2': 'mb', '3': 'ot'}

            old_contact_types = {
                'Primary': ['Blair-Shannon House', 'Freudenberger House', 'Hammons House', 'Hutchens House', 'Kentwood Hall', 'Scholars House', 'Sunvilla Tower', 'Wells House', 'Woods House', 'Monroe'],
                'Billing': ['Blair-Shannon House', 'Freudenberger House', 'Hammons House', 'Hutchens House', 'Kentwood Hall', 'Scholars House', 'Sunvilla Tower', 'Wells House', 'Woods House', 'Monroe'],
                'Receptionist_Blair-Shannon': ['Blair-Shannon House'],
                'Receptionist_Dogwood': [],
                'Receptionist_Freudenberger': ['Freudenberger House'],
                'Receptionist_Hammons': ['Hammons House'],
                'Receptionist_Hutchens': ['Hutchens House'],
                'Receptionist_Kentwood': ['Kentwood Hall'],
                'Receptionist_Scholars': ['Scholars House'],
                'Receptionist_Sunvilla': ['Sunvilla Tower'],
                'Receptionist_Wells': ['Wells House'],
                'Receptionist_Woods': ['Woods House'],
                'Receptionist_Monroe': ['Monroe'],
            }

            contact_types = {}
            for row in c.execute('select contact_type_id, contact_type_name from contact_type'):
                contact_types[str(row[0])] = [Building.objects.get(name=x) for x in old_contact_types[row[1]]]

            for row in c.execute('select contact_name, contact_email, contact_type_id from contacts'):
                contact = Contact.objects.get_or_create(email=row[1], defaults={'name': row[0]})[0]
                contact.buildings = contact_types[str(row[2])]
                contact.alert_statuses = statuses.values()

            for row in c.execute(
                    'select key_req_id, building_id, student_name, amt_rcvd, amt_rcv_type_id, bill_acc, ssn, staff_name, charged_rcr, key_req_type_id, comments, date, cores, types, rooms, key_nums, qtys, status_id, status_update_time, status_update_user from key_req'):
                key_req_id, building_id, student_name, amt_rcvd, amt_rcv_type_id, bill_acc, ssn, staff_name, charged_rcr, key_req_type_id, comments, date, cores, types, rooms, key_nums, qtys, status_id, status_update_time, status_update_user = row

                building = buildings[str(building_id)]
                if ssn:
                    ssn = str(ssn).upper()
                    if 'NA' in ssn:
                        ssn = None
                user = get_user_model().objects.get_or_create(username=status_update_user.lower())[0]
                created_timestamp = convert_timestamp(date)

                req = Request.objects.create(
                    building=building,
                    student_name=student_name,
                    reason_for_request=reasons[str(key_req_type_id)],
                    amt_received=amt_rcvd or 0,
                    payment_method=payment_methods[str(amt_rcv_type_id)],
                    charge_amount=bill_acc or 0,
                    staff=user,
                    bpn=ssn or '',
                    created_timestamp=created_timestamp,
                    charged_on_rcr=bool(charged_rcr),
                    status=statuses[str(status_id)],
                    previous_status=statuses[str(status_id)],
                    locksmith_email_sent=True,
                    updated=True,
                )

                key_datas = []
                for core, type, room, key_num, qty in zip(
                        *[x.split('|') for x in (cores, types, rooms, key_nums, qtys)]):
                    key_datas.append(
                        KeyData(
                            request=req,
                            core_number=core,
                            key_type=key_types[
                                str(type)],
                            room_number=room,
                            key_number=key_num,
                            quantity=''.join(
                                (x for x in qty if x.isdigit())) or 0))
                KeyData.objects.bulk_create(key_datas)

                if comments.strip():
                    Comment.objects.create(
                        request=req,
                        author=user,
                        created_timestamp=created_timestamp,
                        message=comments)


def convert_timestamp(timestamp):
    return make_aware(datetime.fromtimestamp(int(timestamp)), timezone=utc)
