"""
URL configuration for django_delights project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from inventory.views import IngredientListView, IngredientDeleteView, MenuItemListView, PurchaseListView, ProfitRevenueView, AddMenuItemView, AddIngredientView, AddRecipeRequirementView, RecordPurchaseView, UpdateIngredientView, UserLoginView, UserLogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ingredient/', IngredientListView.as_view(), name='ingredient-list'),
    path('ingredient/delete/<int:pk>/', IngredientDeleteView.as_view(), name='ingredient-delete'),
    path('menu/', MenuItemListView.as_view(), name='menuitem-list'),
    path('purchases/', PurchaseListView.as_view(), name='purchase-list'),
    path('profits/', ProfitRevenueView.as_view(), name='profit-revenue'),
    path('add-menu-item/', AddMenuItemView.as_view(), name='add_menu_item'),
    path('add-ingredient/', AddIngredientView.as_view(), name='add_ingredient'),
    path('add-recipe-requirement/', AddRecipeRequirementView.as_view(), name='add_recipe_requirement'),
    path('record-purchase/', RecordPurchaseView.as_view(), name='record_purchase'),
    path('update-ingredient/<int:pk>/', UpdateIngredientView.as_view(), name='update_ingredient'),
    path('', UserLoginView.as_view(), name='login_register'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
