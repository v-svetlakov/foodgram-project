from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserSignUpForm


class SignUp(CreateView):
    form_class = UserSignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/singup.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']

        return super().form_valid(form)
