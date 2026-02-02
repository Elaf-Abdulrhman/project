from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Contact

from django.http import HttpRequest, HttpResponse

# Create your views here.
def contact_us_view(request: HttpRequest):
    if request.method == "POST":
        new_contact = Contact(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            message=request.POST['message']
        )
        new_contact.save()
        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact:contact_us_view')
    return render(request, "contact/contact_us.html")

