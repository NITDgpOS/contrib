import random

from django.test import TestCase, Client
from unittest.mock import patch
from django.urls import reverse

from django.contrib.auth.models import User, AnonymousUser
from core.models import UserProfile
from core.pipeline import save_profile


class UserProfileModelTestCase(TestCase):
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
    def test_when_backend_is_github_and_user_not_present(self, mock_backend):
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
        UserProfile.objects.create(user=self.test_user, name="Test User 2")
        save_profile(mock_backend, self.test_user, self.response)
        self.assertEqual(len(UserProfile.objects.all()), 1)
        self.assertEqual(
            UserProfile.objects.get(user=self.test_user).name,
            "Test User 2"
        )


class HomeViewTestCase(TestCase):
    """Test the HomeView."""

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.test_users = []
        for i in range(13):
            cls.test_users.append(User.objects.create_user(
                username='testuser{}'.format(i+1),
                password='12345678'
            ))
        for user in cls.test_users:
            UserProfile.objects.create(
                user=user,
                contributions=random.randint(70, 401),
                contribution_points=random.randint(100, 1001)
            )

    def test_get_request_to_the_view(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_users_context(self):
        response = self.client.get(reverse('index'))
        queryset = response.context['users']
        ordered_queryset = UserProfile.objects.all().order_by(
            '-contributions', '-contribution_points'
        )[:10]
        self.assertEqual(len(queryset), 10)
        self.assertFalse(response.context['is_authenticated'])
        for i in range(len(queryset)):
            self.assertEqual(
                queryset[i].user.username,
                ordered_queryset[i].user.username
            )

    def test_other_context_when_logged_out(self):
        response = self.client.get(reverse('index'))
        self.assertFalse(response.context['is_authenticated'])
        self.assertTrue(
            isinstance(response.context['current_user'], AnonymousUser)
        )

    def test_other_context_when_logged_in(self):
        self.client.login(username='testuser1', password='12345678')
        response = self.client.get(reverse('index'))
        self.assertTrue(response.context['is_authenticated'])
        self.assertEqual(
            response.context['current_user'].username,
            'testuser1'
        )
