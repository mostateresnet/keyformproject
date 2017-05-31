from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

import string
import random
from keyform.models import *
from django.contrib.auth import get_user_model

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        """
        Made to populate the Keyform database in order to make sure pagination is working
        """


        def add_request():
            name = ''
            user = get_user_model().objects.all()[0]
            building = Building.objects.all()[0]
            for i in range(10):
                name = name + get_letter()
            print(name)
            request = Request(student_name=name, reason_for_request='bk', amt_received=69, charge_amount=0,
            bpn='M23404939', staff=user, building=building, status='pr')
            #request.save()
            return request

        def add_keydata(request):
            room_number = ''
            core_number = ''
            for i in range(5):
                val = random.random()
                if val < .2:
                    room_number = room_number + get_letter()
                else:
                    room_number = room_number + str(get_number())
            print(room_number)
            for i in range(5):
                val = random.random()
                if val < .2:
                    core_number = core_number + get_letter()
                else:
                    core_number = core_number + str(get_number())
            print(core_number)
            keydata = KeyData(request=request, new_core_number=core_number, key_type='rm', room_number=room_number, lost_key_number='23-98y', quantity=1)
            return keydata


        def get_letter():
            return random.choice(string.ascii_letters)


        def get_number():
            return random.randrange(9)


        start = now()
        request_list = []
        for i in range(10000):
            request_list.append(add_request())


        Request.objects.bulk_create(request_list)
        keydata_list = []
        for req in Request.objects.annotate(cnt=models.Count('keydata')).filter(cnt=0):
            keydata_list.append(add_keydata(req))


        KeyData.objects.bulk_create(keydata_list)
        print('Time taken: %s' % (now() - start))
