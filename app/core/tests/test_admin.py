"""
Tests for the Django admin modification
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    """
    Tests for the admin site
    """

    def setUp(self):
        """Create user and client"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            password='<PASSWORD>'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            username='user',
            password='<PASSWORD>',
            email='email@user.com',
            name='name'
        )

    def test_users_list(self):
        """Test that users are listed on the users page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.username)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
