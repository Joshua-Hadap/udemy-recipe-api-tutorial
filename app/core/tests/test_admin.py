from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from core import models


class AdminSiteTest(TestCase):

    def setUp(self):

        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@gmail.com',
            password='Password123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@gmail.com',
            password='Password123',
            name='User Test Name'
        )

    def test_user_listed_page(self):
        """Test if the list of users page is working"""
        
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test if the user chage page is working"""

        url = reverse('admin:core_user_change',args=(self.user.id,))
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_user_add_page(self):
        """Test if the user add page is working"""

        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)