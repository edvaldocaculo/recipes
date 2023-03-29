from django.urls import path

from . import views

urlpatterns = [
    path('', views.RecipeListViewHome.as_view(), name='recipes-home'),
    path('recipes/search/', views.RecipeListViewSearch.as_view(),
         name='search'
         ),
    path('recipes/category/<int:category_id>/',
         views.RecipesListViewCategory.as_view(), name='category'),
    path('recipes/<pk>/', views.RecipeDetail.as_view(), name='recipe-details'),

]
