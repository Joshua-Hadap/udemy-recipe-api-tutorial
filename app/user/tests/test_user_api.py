from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


USER_URL = reverse('user:user-list')
LOGIN_URL = reverse('user:login')

def create_user(**data):
    return get_user_model().objects.create_user(**data)

class LoginApiTest(TestCase):

    def setUp(self):
        
        self.client = APIClient()

    def test_create_user_success(self):

        payload = {
            'email': 'test@gmail.com',
            'password': 'Test123',
            'name': 'Test'
        }

        create_user(**payload)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertEqual(user.email, payload['email'])
        self.assertEqual(user.name, payload['name'])
        self.assertTrue(user.check_password(payload['password']))
    
    def test_user_login_success(self):

        payload = {
            'email': 'test@gmail.com',
            'password': 'Test123',
            'name': 'Test'
        }

        create_user(**payload)
        
        res = self.client.post(LOGIN_URL, data={'email': payload['email'], 'password': payload['password']})
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['email'], payload['email'])
        self.assertEqual(res.data['name'], payload['name'])
        self.assertIn('success',res.data)
    
    def test_user_login_failed(self):

        payload = {
            'email': 'test@gmail.com',
            'password': 'Test123',
            'name': 'Test'
        }

        res = self.client.post(LOGIN_URL, data={'email': payload['email'], 'password': payload['password']})

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_list(self):

        payload = {
            'email': 'test@gmail.com',
            'password': 'Test123',
            'name': 'Test'
        }

        create_user(**payload)
        user = get_user_model().objects.get(email=payload['email'])
        self.client.force_authenticate(user=user)

        login_res = self.client.post(LOGIN_URL, data={'email': payload['email'], 'password': payload['password']})

        self.assertEqual(login_res.status_code, status.HTTP_200_OK)

        user_res = self.client.get(USER_URL)
        
        self.assertEqual(user_res.status_code, status.HTTP_200_OK)
        self.assertContains(user_res, payload['email'])
    
    def test_create_user(self):

        payload = {
            'email': 'test@gmail.com',
            'password': 'Test123',
            'name': 'Test'
        }

        create_user(**payload)
        user = get_user_model().objects.get(email=payload['email'])
        self.client.force_authenticate(user=user)

        login_res = self.client.post(LOGIN_URL, data={'email': payload['email'], 'password': payload['password']})

        self.assertEqual(login_res.status_code, status.HTTP_200_OK)

        another_payload = {
            'email': 'test1@gmail.com',
            'password': 'Test123',
            'name': 'Test1'
        }

        user_res = self.client.post(USER_URL, another_payload)

        self.assertEqual(user_res.status_code, status.HTTP_201_CREATED)
    
    def test_user_details(self):

        payload = {
            'email': 'test@gmail.com',
            'password': 'Test123',
            'name': 'Test'
        }

        create_user(**payload)
        user = get_user_model().objects.get(email=payload['email'])

        self.client.force_authenticate(user=user)

        login_res = self.client.post(LOGIN_URL, data={'email': payload['email'], 'password': payload['password']})

        self.assertEqual(login_res.status_code, status.HTTP_200_OK)

        res = self.client.get(reverse('user:user-detail', args=(user.id,)))

        self.assertEqual(res.status_code, status.HTTP_200_OK)