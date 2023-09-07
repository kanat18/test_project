from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm, UserLoginForm
from .models import UserMessages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from .serializers import UserMessagesSerializer, UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User



def registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            first_name=form.cleaned_data.get('first_name')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password, first_name=first_name)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def main_page(request):
    try:
        context = {
            'user_messages': UserMessages.objects.filter(token=request.user.password)
        }
    except: 
        context = {}

    return render(request, 'index.html', context)


class UserLoginView(SuccessMessageMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'login.html'
    next_page = '/'
    success_message = 'Добро пожаловать на сайт!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация на сайте'
        return context



class UserMessagesList(generics.ListCreateAPIView):
    queryset = UserMessages.objects.all()
    serializer_class = UserMessagesSerializer


class UserMessagesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserMessages.objects.all()
    serializer_class = UserMessagesSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer







