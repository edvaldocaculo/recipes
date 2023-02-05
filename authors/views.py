from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import RegisterForm

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
    return redirect('register')  # URL
