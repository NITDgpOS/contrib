from core.models import UserProfile


def save_profile(backend, user, response, *args, **kwargs):
    """Custom pipeline to set the name of the UserProfile object."""
    if backend.name == 'github':
        try:
            UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(
                user=user, name=response['name'],
                avatar=response['avatar_url']
            )
