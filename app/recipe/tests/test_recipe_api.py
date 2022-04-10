from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from core import models
from recipe import serializers

RECIPE_URL = reverse('recipe:recipe-list')

class PublicRecipeApiTest(TestCase):

    def setUp(self):

        self.client = APIClient()

    def test_login_required(self):

        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeApiTest(TestCase):

    def setUp(self):

        self.user = get_user_model().objects.create_user(email='test@gmail.com',password='Test123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_recipe(self):

        models.Recipe.objects.create(user=self.user, title='Adobo', time_minutes=5, price=5.00)
        models.Recipe.objects.create(user=self.user, title='Sinigang', time_minutes=5, price=5.00)

        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipes = models.Recipe.objects.all().order_by('-title')
        serializer = serializers.RecipeSerializer(recipes, many=True)

        self.assertEqual(res.data, serializer.data)

    def test_retrieve_recipe_detail(self):

        recipe = models.Recipe.objects.create(user=self.user, title='Adobo', time_minutes=5, price=5.00)
        
        res = self.client.get(reverse('recipe:recipe-detail', args=(recipe.id,)))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], recipe.title)

    def test_retrieve_recipe_with_ingridients(self):

        ingridient = models.Ingridient.objects.create(user=self.user,name='Sauce')

        recipe = models.Recipe.objects.create(user=self.user,title='Adobo',time_minutes=5,price=5.00)
        recipe.ingridients.add(ingridient)
        recipe.save()

        res = self.client.get(reverse('recipe:recipe-detail', args=(recipe.id,)))
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['ingridients'][0], ingridient.id)
    
    def test_update_recipe(self):

        recipe = models.Recipe.objects.create(user=self.user,title='Adobo',time_minutes=5,price=5.00)
        
        payload = {
            'title':'Langka',
            'time_minutes': 10
        }

        res = self.client.patch(reverse('recipe:recipe-detail',args=(recipe.id,)),payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], payload['title'])
    
    def test_update_recipe_with_ingridients(self):

        ingridient = models.Ingridient.objects.create(user=self.user,name='Sauce')

        recipe = models.Recipe.objects.create(user=self.user,title='Adobo',time_minutes=5,price=5.00)
        recipe.ingridients.add(ingridient)
        recipe.save()

        new_ingridient = models.Ingridient.objects.create(user=self.user,name='Ketchup')
        payload = {
            'ingridients': new_ingridient.id
        }

        res = self.client.patch(reverse('recipe:recipe-detail', args=(recipe.id,)),payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['ingridients'][0], new_ingridient.id)
        self.assertNotEqual(res.data['ingridients'][0], ingridient.id)