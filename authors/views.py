from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import LoginForms, RegisterForm

# Create your views here.


def register_view(request):
    register_form_data = request.session.get('register_form_data')
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', context={
        'form': form,
        'form_action': reverse('create')
    })


def register_create(request):

    if not request.POST:
        raise Http404
    POST = request.POST
    # salvando o dicionario do post inteiro, cria os dados da sessão
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)
    # salvando o usuario na zona administratva
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(
            request, 'Seu perfil foi criado com sucesso, faça o login')
        del (request.session['register_form_data'])
        return redirect(reverse('login'))
    return redirect('login')  # URL


def login_views(request):
    form = LoginForms()
    return render(request, 'authors/pages/login.html', context={
        'form': form,
        'form_action': reverse('create_login')
    })


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForms(request.POST)
    # login_url = reverse('login')

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(request, 'Your are logged in.')
            login(request, authenticated_user)
        else:
            messages.error(request, 'Invalid credentials')
    else:
        messages.error(request, 'Invalid username or password')

    # return redirect(login_url)
    return redirect(reverse('dashboard'))


@login_required(login_url='login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        return redirect(reverse('login'))

    if request.POST.get('username') != request.user.username:
        return redirect(reverse('login'))

    logout(request)
    return redirect(reverse('login'))


@login_required(login_url='login', redirect_field_name='next')
def dashboard(request):
    return render(request, 'authors/pages/dashboard.html')
