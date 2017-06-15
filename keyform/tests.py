# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client
from django.utils.timezone import datetime, timedelta, now, make_aware, utc, localtime
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

from keyform.models import Building, Request, KeyData, Comment
from keyform.forms import CreateForm

class StandardTestCase(TestCase):

    def setUp(self):

        self.test_date = make_aware(datetime(2015, 1, 1, 16, 1), timezone=utc)


    def create_building(self, name="test building"):
        return Building.objects.get_or_create(name=name)[0]

    def create_request(self, student_name="Fredric", bpn="m11111111", created_timestamp=None,
                        reason=None, building=None, charge_amount=100, staff=None, status=None):

        created_timestamp = created_timestamp or self.test_date
        reason = reason or Request.REQUEST_TYPES[0][0]
        building = building or self.create_building()
        staff = staff or get_user_model().objects.create(username="freddy")
        status = status or Request.STATUS_TYPES[0][0]

        return Request.objects.get_or_create(
            student_name=student_name,
            bpn=bpn,
            charge_amount=charge_amount,
            created_timestamp=created_timestamp,
            reason_for_request=reason,
            building=building,
            staff=staff,
            status=status,
        )[0]

    def create_keydata(self, request=None, new_core_number='1', key_type=None,
                        room_number='42', lost_key_number='2', quantity=1):

        request = request or self.create_request()
        key_type = key_type or KeyData.KEY_TYPES[0][0]

        return KeyData.objects.get_or_create(
            request=request,
            new_core_number=new_core_number,
            key_type=key_type,
            room_number=room_number,
            lost_key_number=lost_key_number,
            quantity=quantity,
        )[0]


class ModelCoverageTest(StandardTestCase):

    def test_building_str_method(self):
        b = self.create_building()
        self.assertEqual(str(Building.objects.get(pk=b.pk)), b.name, "Building object should have been created")

    def test_request_str_method(self):
        r = self.create_request()
        self.assertEqual(str(Request.objects.get(pk=r.pk)), str(r),
                        "Request object should have been created")

    def test_keydata(self):
        k = self.create_keydata()
        self.assertEqual(KeyData.objects.get(pk=k.pk).new_core_number, k.new_core_number,
                        "Keydata object should have been created")

class KeyRequestViewTest(StandardTestCase):

    def setUp(self):
        StandardTestCase.setUp(self)
        self.test_building = self.create_building()
        self.test_request = self.create_request(building=self.test_building)
        self.test_keydata = self.create_keydata(request=self.test_request)

    def get_post_data(self):
        return {
            'building': self.test_building.pk,
            'student_name': 'freddy',
            'reason_for_request': Request.REQUEST_TYPES[0][0],
            'amt_received': 10,
            'payment_method': Request.PAYMENT_TYPES[0][0],
            'charge_amount': 20,
            'bpn': 'm11111111',
            'charged_on_rcr': 'True'
        }

    def test_valid_request_creation_form(self):
        data = self.get_post_data()
        form = CreateForm(data)
        self.assertTrue(form.is_valid(), "Form should have been valid")

    def test_too_short_bpn_request_creation_form(self):
        data = self.get_post_data()
        data['bpn'] = 'm1'
        form = CreateForm(data)
        self.assertFalse(form.is_valid(), "Form should not accept a bpn that is too short")
