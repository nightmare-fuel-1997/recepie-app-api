"""
test for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users"""
        # List of [input_email, expected_output] pairs to test normalization
        # normalize_email() lowercases the DOMAIN part (after @) only
        # The local part (before @) keeps its original case
        sample_emails = [
            # Domain "EXAMPLE.com" ->
            # "example.com" (lowercased)
            ['test1@EXAMPLE.com', 'test1@example.com'],
            # Local "Test2" stays "Test2",
            #  domain "Example.com" -> "example.com"
            ['Test2@Example.com', 'Test2@example.com'],
            # Local "TEST3" stays "TEST3",
            #  domain "EXAMPLE.COM" -> "example.com"
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            # Domain "example.COM" ->
            #  "example.com"
            ['test4@example.COM', 'test4@example.com']
        ]
        # Loop through each test case: email = --
        #  --> input, expected = output
        for email, expected in sample_emails:
            # Create a user with the input email
            user = get_user_model().objects.create_user(email, "sample123")
            # Assert that the saved email matches the--
            # --> expected normalized version
            self.assertEqual(user.email, expected)
