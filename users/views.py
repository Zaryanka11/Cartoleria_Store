from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from products.models import Basket


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
            messages.success(request, 'Вы успешно зарегестрировались!')
            return HttpResponseRedirect(reverse('users:login'))  # возвращает на страницу авторизации
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)


@login_required # декоратор авторизации
def profile(request):  # request содержит информацию по пользователе
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, files=request.FILES,
                               instance=user)  # чтобы пользователь мог обновлять информацию о себе
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=user)  # работа с определённым объектом (пользователем, под которым мы авторизовались)
    baskets = Basket.objects.filter(user=user)
    total_quantity = 0
    total_sum = 0
    for basket in baskets:
        total_quantity += basket.quantity
        total_sum += basket.sum()

    context = {'form': form, 'tittle': 'Store - Личный кабинет',
               'baskets': baskets,
               'total_quantity': total_quantity,
               'total_sum': total_sum,
               }
    return render(request, 'users/profile.html', context)

def logout(request):
    auth.logout(request)
    return  HttpResponseRedirect(reverse('index'))
