"""
Tests for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(
        username='user',
        email='user@example.com',
        password='12345678'):
    return get_user_model().objects.create_user(
        username=username,
        email=email,
        password=password
    )


class ModelTests(TestCase):
    """
    Tests for models
    """

    def test_create_user_with_email_successful(self):
        """
        Test creating a new user with an email is successful
        """
        username = 'user'
        email = '<EMAIL>'
        password = '<PASSWORD>'
        user = get_user_model().objects.create_user(
            username=username,
            email=email,
            password=password
        )
        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        Test the email for a new user is normalized
        """
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.com', 'test4@example.com']
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                username=email, email=email, password='sample')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                username='test', email=None, password='<PASSWORD>')

    def test_new_user_without_username_raises_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                username=None, email='Test', password='<PASSWORD>')

    def test_create_superuser(self):
        """
        Test creating a new superuser
        """
        user = get_user_model().objects.create_superuser(
            username='admin',
            password='<PASSWORD>'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """ Test creating a recipe successfully"""
        user = get_user_model().objects.create_superuser(
            username='admin',
            password='<PASSWORD>'
        )
        recipe = models.Recipe.objects.create(
            title='Test recipe',
            time_minutes=10,
            price=5.00,
            user=user,
            description='Test description'
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Tag1')

        self.assertEqual(str(tag), tag.name)
