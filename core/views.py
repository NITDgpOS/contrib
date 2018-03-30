from django.views.generic import TemplateView
from django.shortcuts import render

from core.forms import RegistrationForm


class HomeView(TemplateView):
    template = 'core/index.html'

    def get(self, request):
        """Handle get requests.
        """
        form = RegistrationForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        """Handle post requests.
        """
        form = RegistrationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            form = RegistrationForm()
            message = "Hello {}! You have been registered!".format(username)
            args = {'form': form, 'message': message}
            return render(request, self.template, args)

        return render(request, self.template, {'form': form})
