from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DeleteView, TemplateView, UpdateView
from django.views.generic.edit import CreateView
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from .models import Ingredient, MenuItem, Purchase
from .forms import MenuItemForm, IngredientForm, RecipeRequirementForm, PurchaseForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login

class IngredientListView(ListView):
    model = Ingredient
    template_name = 'ingredient_list.html'

class IngredientDeleteView(DeleteView):
    model = Ingredient
    success_url = reverse_lazy('ingredient-list')
    template_name = 'ingredient_confirm_delete.html'

class MenuItemListView(ListView):
    model = MenuItem
    template_name = 'menuitem_list.html'

class PurchaseListView(ListView):
    model = Purchase
    template_name = 'purchase_list.html'

class ProfitRevenueView(TemplateView):
    template_name = 'profit_revenue.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['revenue'] = Purchase.overall_revenue()
        context['cost'] = Purchase.overall_cost()
        context['profit'] = Purchase.overall_profit()
        return context
    
class AddMenuItemView(LoginRequiredMixin, CreateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = "inventory/add_menu_item.html"
    success_url = 'add-menu-item/'

class AddIngredientView(LoginRequiredMixin, CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = "inventory/add_ingredient.html"
    success_url = 'add-ingredient/'

class AddRecipeRequirementView(LoginRequiredMixin, CreateView):
    model = RecipeRequirementForm
    form_class = RecipeRequirementForm
    template_name = "inventory/add_recipe_requirement.html"
    success_url = 'add-recipe-requirement/'

class RecordPurchaseView(LoginRequiredMixin, CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = "inventory/record_purchase.html"
    success_url = 'add-recipe-requirement/'

class UpdateIngredientView(LoginRequiredMixin, UpdateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = "inventory/update_ingredient.html"
    success_url = 'update-ingredient/<int:pk>/'

class UserLoginView(View):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        context = {
            'login_form': AuthenticationForm(),
            'register_form': UserCreationForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')

        if action == 'login':
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('ingredient/')  

        elif action == 'register':
            register_form = UserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                # Log the user in immediately after registration
                login(request, user)
                return redirect('')  

        # If any form is invalid or any other scenario, re-render the template with the forms
        context = {
            'login_form': AuthenticationForm(request, data=request.POST),
            'register_form': UserCreationForm(request.POST),
        }
        return render(request, self.template_name, context)

class UserLogoutView(LogoutView):
    next_page = '/'