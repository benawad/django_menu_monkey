from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout


def register_view(request):
    if request.method == 'GET':
        register_form = UserCreationForm()
    elif request.method == 'POST':
        register_form = UserCreationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            auth_user = authenticate(username=user.username, password=request.POST['password1'])
            login(request, auth_user)
            return HttpResponseRedirect(reverse('index'))

    return render(request, 'accounts/register.html', {'register_form': register_form})


def login_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('index'))
        login_form = AuthenticationForm()
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            login_form = AuthenticationForm()
        
    return render(request, 'accounts/login.html', {'login_form': login_form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
