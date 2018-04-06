from core.models import UserProfile
from core.utils import update_contributions


def reset_contributions():
    """Function for resetting the contributions of all users every month."""
    for user in UserProfile.objects.all():
        user.contributions = 0
        user.contribution_points = 0
        user.last_updated = None
        user.save()


def update_user_contributions():
    """Function to call update_contributions() function on every user daily."""
    for user in UserProfile.objects.all():
        update_contributions(user)
