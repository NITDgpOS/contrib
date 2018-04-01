from django.views.generic import TemplateView
from django.shortcuts import render

from core.models import UserProfile


class HomeView(TemplateView):
    template = 'core/index.html'

    def get(self, request):
        """Handle get requests to the homepage.
        """
        users = UserProfile.objects.all()
        context = {
            'is_authenticated': False,
            'users': users.order_by('-contributions', '-contribution_points')
        }
        if request.user.is_authenticated:
            context['is_authenticated'] = True
            context['current_user'] = request.user
        return render(request, self.template, context)
