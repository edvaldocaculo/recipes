from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from authors.forms import LoginForms, RegisterForm
from authors.forms.recipe_form import AuthorRecipeForm
from recipes.models import Recipe

# Create your views here.


def register_view(request):
    register_form_data = request.session.get('register_form_data')
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', context={
        'form': form,
        'form_action': reverse('create')  # URL
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
    POST = request.POST
    form = LoginForms(POST)
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


# ---------------------------------------------------------------------------------------------
# Visualizar a dashboard do usuario
# ---------------------------------------------------------------------------------------------

@login_required(login_url='login', redirect_field_name='next')
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user
    ).order_by('-id')
    return render(
        request,
        'authors/pages/dashboard.html',
        context={
            'recipes': recipes,
        }
    )

# ----------------------------------------------------------------
# função para Editar a recipe
# ----------------------------------------------------------------


@login_required(login_url='login', redirect_field_name='next')
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id,
    ).first()
    if not recipe:
        raise Http404()

    # cria um formulário que pode receber uma receita ou não,
    # e posssui/recebe uma instância recipe
    form = AuthorRecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    if form.is_valid():
        # Agora, o form é válido e eu posso tentar salvar na zona do admin
        recipe = form.save(commit=False)
        # dados que não foram usados no form de recipes para serem editados
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False

        recipe.save()

        messages.success(request, 'Sua receita foi salva com sucesso!')
        # Redireciona a resposta atraves da url
        return redirect(reverse('dashboard_recipe_edit', args=(id,)))
    return render(
        request,
        'authors/pages/dashboard_recipe.html',
        context={
            "form": form
        }
    )

# ------------------------------------------------------------
# Criar uma nova recipe
# ------------------------------------------------------------


"""
@login_required(login_url='login', redirect_field_name='next')
def dashboard_recipe_new(request):
    form = AuthorRecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        recipe = form.save(commit=False)

        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False

        recipe.save()

        messages.success(request, 'Salvo com sucesso!')
        return redirect(
            reverse('dashboard_recipe_edit', args=(recipe.id,))
        )

    return render(
        request,
        'authors/pages/dashboard_recipe.html',
        context={
            'form': form,
            'form_action': reverse('dashboard_recipe_new')
        }
    )
"""
# -------------------------------------------------------------
# Apagar uma receita
# -------------------------------------------------------------


@login_required(login_url='login', redirect_field_name='next')
def dashboard_recipe_delete(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    id = POST.get('id')
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id,
    ).first()

    if not recipe:
        raise Http404()

    recipe.delete()
    messages.success(request, 'Deleted successfully.')
    return redirect(reverse('dashboard'))
