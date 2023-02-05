
import os

# from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

from utils.pagination import make_pagination

from .models import Recipe

PER_PAGES = os.environ.get('PER_PAGES', 4)


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True
    ).order_by('-id')
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGES)
    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range
    })


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True
        ).order_by('-id')
    )
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGES)
    return render(request, 'recipes/pages/category.html', context={
        'title': f'{recipes[0].category.name} - -Category| ',
        'recipes': page_obj,
        'pagination_range': pagination_range
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

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGES)
    return render(request, 'recipes/pages/search_info.html', context={
        'page_title': f'search for "{search_term}"',
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&search={search_term}',
    })
