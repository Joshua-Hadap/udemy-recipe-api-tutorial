from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from recipe import serializers
from core import models


INGRIDIENT_URL = reverse('recipe:ingridient-list')

class PublicIngridientApiTest(TestCase):

    def setUp(self):

        self.client = APIClient()

    def test_login_required(self):

        res = self.client.get(INGRIDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateIngridientAPITest(TestCase):

    def setUp(self):

        self.user = get_user_model().objects.create_user(email='test@gmail.com',password='Test123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_retrieve_ingridient(self):

        models.Ingridient.objects.create(user=self.user,name='Powder')
        models.Ingridient.objects.create(user=self.user,name='Sauce')

        res = self.client.get(INGRIDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        ingridients = models.Ingridient.objects.order_by('-name').all()
        serializer = serializers.IngridientSerializer(ingridients, many=True)

        self.assertEqual(res.data, serializer.data)

    def test_ingridients_limited_to_user(self):

        user2 = get_user_model().objects.create(email='Test2@gmail.com', password='Test123')
        
        ingridient = models.Ingridient.objects.create(user=self.user,name='Sauce')
        models.Ingridient.objects.create(user=user2,name='Powder')

        res = self.client.get(INGRIDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        ingridients = models.Ingridient.objects.filter(user=self.user).order_by('-name')
        serializer = serializers.IngridientSerializer(ingridients, many=True)

        self.assertEqual(res.data, serializer.data)

    def test_create_valid_ingridient(self):

        payload = {
            'user':self.user.id,
            'name':'Sauce'
        }

        res = self.client.post(INGRIDIENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        exists = models.Ingridient.objects.filter(user=self.user,name=payload['name']).exists()

        self.assertTrue(exists)

    def test_create_invalid_ingridient(self):

        payload = {
            'name':'Sauce'
        }

        res = self.client.post(INGRIDIENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ingridient_str(self):

        ingridient = models.Ingridient.objects.create(user=self.user,name='Sauce')

        self.assertEqual(str(ingridient), 'Sauce')