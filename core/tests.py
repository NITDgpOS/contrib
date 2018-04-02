from django.test import TestCase
from unittest.mock import patch

from django.contrib.auth.models import User
from core.models import UserProfile
from core.pipeline import save_profile


class UserProfileTestCase(TestCase):
    """Test the UserProfile model."""

    def setUp(self):
        test_user = User.objects.create_user(
            username='testuser',
            password='12345678'
        )
        self.test_userprofile = UserProfile.objects.create(
            user=test_user,
            name='Test User'
        )

    def test_user_label(self):
        self.assertTrue(isinstance(self.test_userprofile.user, User))
        self.assertEqual(str(self.test_userprofile.user), 'testuser')

    def test_name_label(self):
        self.assertTrue(isinstance(self.test_userprofile.name, str))
        self.assertEqual(self.test_userprofile.name, 'Test User')

    def test_contributions_label(self):
        self.assertTrue(isinstance(self.test_userprofile.contributions, int))
        self.assertEqual(self.test_userprofile.contributions, 0)

    def test_contribution_points_label(self):
        self.assertTrue(
            isinstance(self.test_userprofile.contribution_points, int)
        )
        self.assertEqual(self.test_userprofile.contribution_points, 0)

    def test_object_name_is_username(self):
        self.assertEqual(self.test_userprofile.user.username,
                         str(self.test_userprofile))


class SaveProfilePipelineTestCase(TestCase):
    """Test the save_profile pipeline."""

    def setUp(self):
        self.response = {'name': "Test User"}
        self.test_user = User.objects.create_user(
            username='testuser',
            password='12345678'
        )

    @patch('social_core.backends.github.GithubOAuth2')
    def test_when_backend_is_not_github(self, mock_backend):
        mock_backend.name = ''
        save_profile(mock_backend, self.test_user, self.response)
        self.assertEqual(len(UserProfile.objects.all()), 0)

    @patch('social_core.backends.github.GithubOAuth2')
    def test_when_backend_is_github_and_user_is_not_present(self, mock_backend):
        mock_backend.name = 'github'
        save_profile(mock_backend, self.test_user, self.response)
        self.assertEqual(len(UserProfile.objects.all()), 1)
        self.assertEqual(
            UserProfile.objects.get(user=self.test_user).name,
            "Test User"
        )

    @patch('social_core.backends.github.GithubOAuth2')
    def test_when_backend_is_github_and_user_is_present(self, mock_backend):
        mock_backend.name = 'github'
        test_userprofile = UserProfile.objects.create(
            user=self.test_user,
            name="Test User 2"
        )
        save_profile(mock_backend, self.test_user, self.response)
        self.assertEqual(len(UserProfile.objects.all()), 1)
        self.assertEqual(
            UserProfile.objects.get(user=self.test_user).name,
            "Test User 2"
        )
