from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import UserProfile, Repository
from core.utils import get_repositories, update_contributions


@receiver(post_save, sender=UserProfile)
def complete_signup(sender, **kwargs):
    """Save the repositories of a user when its UserProfile object is saved and
    update his contributions."""
    if kwargs['created']:
        username = kwargs['instance'].user.username
        repos = get_repositories(username)
        for repo in repos:
            Repository.objects.create(
                owner=kwargs['instance'],
                repo=repo['full_name'],
                is_fork=repo['fork']
            )
        update_contributions(kwargs['instance'])
