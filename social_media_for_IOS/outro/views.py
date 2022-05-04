from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *

base_context = {'app_title': 'IOS-Разработка', 'app_name': 'IOS-Разработка социальная сеть'}


@login_required(login_url='/login/')
def index(request):
    # user = CustomUser.objects.create_user(username='root', email='root@edu.hse.ru', password='root', accepted=True,
    #                                       role='teacher')
    # user.save()
    context = dict(base_context)
    user = CustomUser.objects.filter(email=request.user.email)[0]
    context['name'] = user.username
    return render(request, 'index.html', context)


def register(request):
    context = dict(base_context)
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            mail, password, username, role = form.data['email'], form.data['password'], form.data['username'],\
                                             form.data['role']
            registered_users = CustomUser.objects.filter(email=mail)
            if registered_users:
                context['message'] = 'Пользователь с таким e-mail уже есть'
            elif CustomUser.objects.filter(username=username).exists():
                context['message'] = 'Пользователь с таким именем уже есть'
            else:
                if role == 'Student' or role == 'student':
                    user = CustomUser.objects.create_user(username=username, email=mail, password=password, role=role,
                                                          accepted=True)
                    user.save()
                    user = authenticate(request, username=mail, password=form.data['password'])
                    if user is not None:
                        login(request, user)
                        return redirect('/')
                else:
                    user = CustomUser.objects.create_user(username=username, email=mail, password=password, role=role,
                                                          accepted=False)
                    user.save()
                    context['message'] = 'Заявка отправлена на проверку администратору'
    else:
        form = RegisterForm()
    context['form'] = form
    return render(request, 'register.html', context)


def log_in(request):
    context = dict(base_context)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.data['email'], password=form.data['password'])
            if user is not None:
                if not CustomUser.objects.filter(email=user.email)[0].accepted:
                    context['message'] = 'Ваш аккаунт ещё не подтверждён администратором'
                    form = LoginForm()
                    context['form'] = form
                    return render(request, 'login.html', context)
                login(request, user)
                context['message'] = 'Вход выполнен'
                return redirect('/')
            context['message'] = 'Не получилось войти'
    else:
        form = LoginForm()
    context['form'] = form
    return render(request, 'login.html', context)


@login_required(login_url='/login/')
def profile(request):
    context = dict(base_context)
    user = CustomUser.objects.filter(email=request.user.email)[0]
    context['name'] = user.username
    context['email'] = user.email
    context['role'] = user.role
    context['picture'] = user.picture
    return render(request, 'profile.html', context)


@login_required(login_url='/login/')
def edit_profile(request):
    context = dict(base_context)
    if request.method == 'POST':
        user = CustomUser.objects.filter(email=request.user.email)[0]
        form = EditUserForm(request.POST)
        if form.is_valid():
            password, username, picture = form.data['password'], form.data['username'], form.data['picture']
            if password is not None and password != '':
                user.password = password
            if username is not None and username != '':
                if CustomUser.objects.filter(username=username).exists():
                    context['message'] = 'Пользователь с таким именем уже существует'
                    form = EditUserForm()
                    context['form'] = form
                    return render(request, 'edit-profile.html', context)
                user.username = username
            if picture is not None and picture != '':
                user.picture = picture
            user.save()
            login(request, user)
            return redirect('/profile/')
        else:
            context['message'] = 'Неправильные данные'
    else:
        form = EditUserForm()
    context['form'] = form
    return render(request, 'edit-profile.html', context)


@login_required
def log_out(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/login/')
def accept_user(request, email):
    user = CustomUser.objects.filter(email=request.user.email)
    if not user.exists():
        return redirect('/login/')
    user = user[0]
    if user.role != 'teacher':
        return HttpResponseForbidden('Доступ к этому разделу только у учителя')
    user_to_accept = CustomUser.objects.filter(email=email)
    if user_to_accept is not None:
        user_to_accept = user_to_accept[0]
        user_to_accept.accepted = True
        user_to_accept.save()
    return redirect('/users/')


@login_required(login_url='/login/')
def refuse_user(request, email):
    user = CustomUser.objects.filter(email=request.user.email)
    if not user.exists():
        return redirect('/login/')
    user = user[0]
    if user.role != 'teacher':
        return HttpResponseForbidden('Доступ к этому разделу только у учителя')
    user_to_refuse = CustomUser.objects.filter(email=email)
    if user_to_refuse is not None:
        user_to_refuse = user_to_refuse[0]
        if user_to_refuse.email == user.email:
            return HttpResponse('Невозможно удалить себя')
        user_to_refuse.delete()
    return redirect('/users/')


@login_required(login_url='/login/')
def users(request):
    context = dict(base_context)
    user = CustomUser.objects.filter(email=request.user.email)
    if not user.exists():
        return redirect('/login/')
    user = user[0]
    if user.role != 'teacher':
        return HttpResponseForbidden('Доступ к этому разделу только у учителя')
    context['not_accepted_users'] = CustomUser.objects.filter(accepted=False)
    context['accepted_users'] = CustomUser.objects.filter(accepted=True)
    return render(request, 'users.html', context)
