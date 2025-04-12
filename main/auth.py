from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

def logout_view(request):
    """
    Custom logout view that logs out the user, displays a success message,
    and redirects to the home page.
    """
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home') 