from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')


def detail_url(ingredient_id):
    return reverse('recipe:ingredient-detail', args=(ingredient_id,))


def create_user(
        username='user',
        email='user@example.com',
        password='12345678'):
    return get_user_model().objects.create_user(
        username=username,
        email=email,
        password=password
    )


class PublicTagsApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        Ingredient.objects.create(user=self.user, name='Apple')
        Ingredient.objects.create(user=self.user, name='Orange')

        res = self.client.get(INGREDIENTS_URL)

        tags = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        user2 = create_user(
            username='user2',
            email='<EMAIL>',
            password='<PASSWORD>'
        )
        Ingredient.objects.create(user=user2, name='Apple')
        tag = Ingredient.objects.create(user=self.user, name='Orange')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['id'], tag.id)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_update_ingredient(self):
        ingredient = Ingredient.objects.create(user=self.user, name='Apple')
        payload = {'name': 'Orange'}

        res = self.client.patch(detail_url(ingredient.id), payload)
        ingredient.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(ingredient.name, payload['name'])

    def test_delete_ingredient(self):
        tag = Ingredient.objects.create(user=self.user, name='Apple')

        res = self.client.delete(detail_url(tag.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ingredient.objects.filter(user=self.user).exists())
