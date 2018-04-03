from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import UserProfile, Repository
from core.utils import get_repositories


@receiver(post_save, sender=UserProfile)
def save_repositories(sender, **kwargs):
    """Save the repositories of a user when its UserProfile object is saved."""
    if kwargs['created']:
        username = kwargs['instance'].user.username
        repos = get_repositories(username)
        for repo in repos:
            Repository.objects.create(
                owner=kwargs['instance'],
                repo=repo['full_name'],
                is_fork=repo['fork']
            )
