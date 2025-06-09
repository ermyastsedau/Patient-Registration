from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from .forms import CustomUserCreationForm

User = get_user_model()  # Always use this to refer to your CustomUser model


# Custom logout view
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

# Optional: Role check for SYSTEM_ADMIN
def is_system_admin(user):
    return user.is_authenticated and user.role == 'SYSTEM_ADMIN'

# View to register a new user
# Uncomment the decorators below to restrict access to SYSTEM_ADMIN only
# @login_required
# @user_passes_test(is_system_admin)
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, CustomUserEditForm

User = get_user_model()

def manage_user(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid method'})
    
    user_id = request.POST.get('user_id')
    is_edit = bool(user_id)
    
    if is_edit:
        # Edit existing user
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found'})
        
        form = CustomUserEditForm(request.POST, instance=user)
    else:
        # Create new user
        form = CustomUserCreationForm(request.POST)
    
    if form.is_valid():
        user = form.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({
            'success': False, 
            'error': form.errors.as_json()
        })


# View to list users
# Uncomment the decorators below to restrict access to SYSTEM_ADMIN only
# @login_required
# @user_passes_test(is_system_admin)
def user_list(request):
    users = User.objects.all()
    return render(request, 'accounts/user_list.html', {'users': users})

def logoutview(request):
    logout(request)
    return redirect('login')

def login_user(request):
    print("Login view called")
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        print("POST received")  # Debug

        username = request.POST.get('username')
        password = request.POST.get('password')

        print(f"Username: {username}, Password: {password}")  # Debug

        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            print("User authenticated")  # Debug
            login(request, validate_user)
            return redirect('home')
        else:
            print("Invalid credentials")  # Debug
            messages.error(request, 'Error, Wrong user detail')
            return redirect('login')
    return render(request, 'accounts/login.html', {})