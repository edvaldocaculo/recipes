from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

from .models import Recipe


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True
    ).order_by('-id')

    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
    })


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True
        ).order_by('-id')
    )
    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
        'title': f'{recipes[0].category.name} - -Category| '
    })


def recipe(request, id):
    recipe = get_object_or_404(
        Recipe.objects.filter(
            pk=id,
            is_published=True
        )
    )
    return render(request, 'recipes/pages/recipe-views.html', context={
        'recipe': recipe,
        'is_details_page': True,
    })


def search(request):
    search_term = request.GET.get('search', '').strip()
    recipes = Recipe.objects.filter(
        Q(Q(title__contains=search_term) |
          Q(description__contains=search_term)), is_published=True
    ).order_by('-id')
    if not search_term:
        raise Http404()

    return render(request, 'recipes/pages/search_info.html', context={
        'page_title': f'search for "{search_term}"',
        'recipes': recipes,
    })
