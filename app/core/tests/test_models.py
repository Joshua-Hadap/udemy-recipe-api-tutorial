from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='sample@gmail.com',password='sample123'):
    return get_user_model().objects.create_user(email=email,password=password)

class ModelTestCase(TestCase):

    def test_create_user_with_email_successful(self):
        """Creating new user with email successfully"""

        email = 'test@gmail.com'
        password = 'Test123'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))

    def test_new_user_invalid_email(self):
        """Test creating a new user with invalid email"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None,'Test123')

    def test_create_new_superuser(self):
        """Create a new superuser"""

        email = 'test@gmail.com'
        password = 'Test123'

        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_tag_string_representation(self):

        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)