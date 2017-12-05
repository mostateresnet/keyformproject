from django.test import TestCase, Client
from django.utils.timezone import datetime, timedelta, make_aware, utc
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from keyform.models import Building, Status, Request, KeyData

class StandardTestCase(TestCase):

    def setUp(self):

        self.test_date = make_aware(datetime(2017, 1, 1, 16, 1), timezone=utc)

        users = [('nu', 'normaluser'), ('cu', 'contactuser')]

        self.clients = {}

        for user,_ in users:
            # import pdb; pdb.set_trace()
            self.clients[user] = Client()
            self.clients[user].user_object = get_user_model().objects.create(username=user)
            self.clients[user].force_login(self.clients[user].user_object)


    def create_building(self, name="Test Building", deleted=False):
        return Building.objects.get_or_create(name=name, deleted=deleted)[0]

    def create_status(self, name="Test Status", visible=True, order=0):
        return Status.objects.get_or_create(name=name, visible=visible, order=order)[0]

    def create_request(self, staff=None):
        start = self.test_date
        #end = (self.test_date + timedelta(days=1))
        if staff is None:
            staff = self.clients['nu'].user_object

        request = Request.objects.get_or_create(
            building=self.create_building(),
            student_name="Test Student",
            reason_for_request=Request.REQUEST_TYPES[0][0],
            amt_received=0,
            payment_method=Request.PAYMENT_TYPES[0][0],
            charge_amount=0,
            staff=staff,
            bpn='M12345678',
            created_timestamp=start,
            charged_on_rcr=False,
            status=self.create_status(),
            previous_status=self.create_status(),
            locksmith_email_sent=True,
            updated=True,
        )[0]

        return request

    def create_keydata(self, request):
        keydata = KeyData.objects.get_or_create(
            request = request,
            key_type = KeyData.KEY_TYPES[0][0],
            room_number = 'Test Room',
            key_number = 'Test Number',
            quantity = 1
        )[0]

        return keydata




class ModelCoverageTest(StandardTestCase):

    def test_building_str_method(self):
        b = self.create_building()
        self.assertEquals(str(Building.objects.get(pk=b.pk)), b.name, "Building object should have been created")

    def test_status_str_method(self):
        s = self.create_status()
        self.assertEquals(str(Status.objects.get(pk=s.pk)), s.name, "Status object should have been created")

    def test_request_str_method(self):
        pass

    def test_keydata_str_method(self):
        pass

    def test_comment_str_method(self):
        pass

    def test_contact_str_method(self):
        pass

class HomeViewTest(StandardTestCase):

    def test_gets_create(self):
        response = self.clients['nu'].get(reverse('home'))
        self.assertEquals(response.status_code, 200, "The home page should have been loaded")
