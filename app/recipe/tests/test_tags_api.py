from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from core import models
from recipe import serializers

TAGS_URL = reverse('recipe:tag-list')

class PublicTagsApiTest(TestCase):

    def setUp(self):

        self.client = APIClient()

    def test_login_required(self):

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateTagsApiTest(TestCase):

    def setUp(self):

        self.user = get_user_model().objects.create_user(email='test@gmail.com',password='Test123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_tags(self):

        models.Tag.objects.create(user=self.user,name='Vegan')
        models.Tag.objects.create(user=self.user,name='Meat')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        tags = models.Tag.objects.order_by('-name').all()
        serializer = serializers.TagSerializer(tags, many=True)

        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):

        user2 = get_user_model().objects.create_user(email='test2@gmail.com',password='Test123')

        models.Tag.objects.create(user=user2,name='Vegan')
        tag = models.Tag.objects.create(user=self.user,name='Carnivor')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_valid_tag(self):

        payload = {
            'user': self.user.id,
            'name':'Vegan'
        }

        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        exists = models.Tag.objects.filter(user=self.user,name=payload['name']).exists()
        self.assertTrue(exists)

    def test_create_invalid_tag(self):

        payload = {
            'name':'Vegan'
        }

        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)