from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    contributions = models.IntegerField(default=0)
    contribution_points = models.IntegerField(default=0)
    last_updated = models.DateTimeField(null=True)
    avatar = models.URLField(max_length=150, null=True)

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
