"""
URL configuration for Sportify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import settings
from django.views.i18n import set_language


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('account/', include('account.urls')),
    path('contact/', include('contact.urls')),
    path('posts/', include('posts.urls')),
    path('offers/', include('offers.urls')),
    path('athlete/', include('athlete.urls')),
    path('clubs/', include('clubs.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    path('bookmarks/', include('bookmarks.urls')),
    path('admins/', include('admins.urls')),
    path('direct_message/', include('direct_message.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
