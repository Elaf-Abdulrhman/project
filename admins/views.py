from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    if request.user.is_superuser:

        return render(request, 'admins/dashboard.html')
    else:

        return render(request, 'admins/notadmin.html')

# def to_dashboard(request):
#     return redirect('admins:dashboard')