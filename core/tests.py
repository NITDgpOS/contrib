from django.test import TestCase

from django.contrib.auth.models import User
from core.models import UserProfile


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
