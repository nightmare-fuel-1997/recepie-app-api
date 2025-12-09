"""
tests for admin functionalities.
"""
# Base test case class for writing Django tests
from django.test import TestCase
# Function to get the active user model (supports custom user models)
from django.contrib.auth import get_user_model
# Utility to generate URLs from URL patterns defined in urls.py
from django.urls import reverse
# Test client for simulating HTTP requests (GET, POST, etc.)
from django.test import Client


class AdminSiteTests(TestCase):
    """Tests for admin site functionalities."""

    def setUp(self):
        """create user and client for tests."""
        # Initialize the test client
        self.client = Client()
        # Get the User model (supports custom user models)
        self.User = get_user_model()
        # Create a superuser for admin access
        self.admin_user = self.User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='userpass123',
            name='Test User'
        )

    def test_users_listed(self):
        """Test that users are listed on user page."""
        # Generate the URL for the user list page in admin
        url = reverse('admin:core_user_changelist')
        # Make a GET request to the user list page
        res = self.client.get(url)

        # Check that the response contains the user's name and email
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_users_list(self):
        """Test that edit user page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.user.name)
