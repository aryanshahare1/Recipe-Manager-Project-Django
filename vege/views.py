from django.shortcuts import render, redirect
from .models import *
from django.urls import reverse
from django.contrib import messages 
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required



def home(request):  
    return render(request, 'home.html')


@login_required(login_url='/login/')
def recipes(request):
    queryset = Recipe.objects.all()

    # Search logic
    if request.GET.get('search'):
        queryset = queryset.filter(recipe_name__icontains=request.GET.get('search'))
        
    context = {'recipes': queryset}
    return render(request, 'recipes.html', context)


@login_required(login_url='/login/')
def add_recipe(request):
    if request.method == "POST":
        data = request.POST
        recipe_image = request.FILES.get('recipe_image')
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')

        Recipe.objects.create(
            recipe_image=recipe_image,
            recipe_name=recipe_name,
            recipe_description=recipe_description
        )
        messages.success(request, "Recipe added successfully!") 
        return redirect('/recipes')
    
    return render(request, 'add_recipe.html')

def update_recipe(request, id):
    queryset = Recipe.objects.get(id=id)

    if request.method == "POST":
        data = request.POST
        recipe_image = request.FILES.get('recipe_image')
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')

        queryset.recipe_name = recipe_name
        queryset.recipe_description = recipe_description

        if recipe_image:
            queryset.recipe_image = recipe_image

        queryset.save()
        messages.success(request, "Recipe updated successfully!")  
        return redirect('/recipes')

    context = {'recipe': queryset}
    return render(request, 'update_recipes.html', context)

def delete_recipe(request, id):
    queryset = Recipe.objects.get(id=id)
    queryset.delete()
    messages.success(request, "Recipe deleted successfully!") 
    return redirect('/recipes')


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return redirect(reverse('login_page'))  # Use reverse for redirection

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid password')
            return redirect(reverse('login_page'))  # Use reverse for redirection

        login(request, user)
        return redirect(reverse('recipes'))  # Use reverse for redirection to recipes

    return render(request, 'login.html')


def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)

        if user.exists():
            messages.info(request, "Username already taken!")
            return redirect('/register/')

        user = User.objects.create_user(username=username, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        messages.success(request, "Account created successfully! Please log in.")

        return redirect('/login/')

    return render(request, 'register.html')


def logout_page(request):
    logout(request)
    return redirect(reverse('login_page'))