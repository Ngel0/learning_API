from .forms import SignUpForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


class SignUp(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('cryptocurrency_list')
    template_name = 'register/signup.html'
