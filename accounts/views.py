from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserRegistrationForm
from .models import User


class SignupView(CreateView):
    template_name = "products/forms/form.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("login")
