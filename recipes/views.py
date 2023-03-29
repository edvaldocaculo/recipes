
import os

from django.db.models import Q
from django.http import Http404
from django.views.generic import DetailView, ListView

from utils.pagination import make_pagination

from .models import Recipe

PER_PAGES = os.environ.get('PER_PAGES', 4)


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('recipes'),
            PER_PAGES
        )
        ctx.update(
            {'recipes': page_obj, 'pagination_range': pagination_range}
        )
        return ctx


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipesListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category__id=self.kwargs.get('category_id'),
            is_published=True
        )
        if not qs:
            raise Http404
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('recipes'),
            PER_PAGES
        )
        ctx.update(
            {'recipes': page_obj, 'pagination_range': pagination_range,
             'title': f'{ctx.get("recipes")[0].category.name} - -Category| '
             }
        )
        return ctx


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search_info.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('search', '')
        if not search_term:
            raise Http404
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term),
            )
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('search', '')

        ctx.update({
            'page_title': f'Search for "{search_term}" |',
            'search_term': search_term,
            'additional_url_query': f'&search={search_term}',
        })

        return ctx


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-views.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'is_detail_page': True
        })
        return ctx
