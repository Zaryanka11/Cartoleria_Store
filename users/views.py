from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm


def login(request):  # логика авторизации
    if request.method == 'POST':  # словарик с данными
        form = UserLoginForm(data=request.POST)  # словарик с ключом и значением (user, password)
        if form.is_valid():  # проверяет, корректны ли введённые данные
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:  # проверяем, есть ли пользователь в базе данных, удалён он или нет
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))  # перенапрвление пользователя после регистрации
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()  # сохраняются данные в базе
            return HttpResponseRedirect(reverse('users:login'))  # возвращает на страницу авторизации
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)


def profile(request):  # request содержит информацию по пользователе
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, files=request.FILES,
                               instance=request.user)  # чтобы пользователь мог обновлять информацию о себе
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(
            instance=request.user)  # работа с определённым объектом (пользователем, под которым мы авторизовались)
    context = {'form': form}
    return render(request, 'users/profile.html', context)
