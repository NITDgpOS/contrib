from django.views.generic.list import ListView

from core.models import UserProfile


class HomeView(ListView):
    template_name = 'core/index.html'
    context_object_name = 'users'

    def get_queryset(self):
        return UserProfile.objects.all().order_by(
            '-contributions', '-contribution_points'
        )[:10]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['current_user'] = self.request.user
        return context
