from django.views.generic import TemplateView
from django.shortcuts import render


class HomeView(TemplateView):
    template = 'core/index.html'

    def get(self, request):
        """Handle get requests to the homepage.
        """
        context = {'is_authenticated': False}
        if request.user.is_authenticated:
            context['is_authenticated'] = True
            context['user'] = request.user
        return render(request, self.template, context)
