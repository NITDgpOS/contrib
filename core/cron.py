from core.models import UserProfile

def reset_contributions():
    """Reset the contributions of all users on the 1st of every month."""
    for user in UserProfile.objects.all():
        user.contributions = 0
        user.contribution_points = 0
        user.last_updated = None
        user.save()
