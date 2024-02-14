from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import ListView, DetailView

from accounts.models import Profile


# Create your views here.
class SignUpForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        #fields = '__all__'
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('index')
    template_name = 'signup.html'


# TODO: ProfileCreate
# TODO: ProfileUpdate
# TODO: ProfileDelete

class ProfileListView(ListView):
    template_name = 'profiles.html'
    model = Profile
    paginate_by = 10
    context_object_name = 'profiles'


class ProfileDetailView(DetailView):
    pass
