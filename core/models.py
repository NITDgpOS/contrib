import requests

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    contributions = models.IntegerField(default=0)
    contribution_points = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Repository(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    repo = models.CharField(max_length=100)
    is_fork = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Repositories'

    def __str__(self):
        return self.repo


@receiver(post_save, sender=UserProfile)
def save_repositories(sender, instance, created, **kwargs):
    """Save the repositories of a user when its UserProfile object is saved."""
    if created:
        username = instance.user.username
        repos_url = 'https://api.github.com/users/{}/repos'.format(username)
        response = requests.get(repos_url)
        repos = []
        if response.status_code == 200:
            repos = response.json()
        for repo in repos:
            Repository.objects.create(
                owner=instance,
                repo=repo['full_name'],
                is_fork=repo['fork']
            )
