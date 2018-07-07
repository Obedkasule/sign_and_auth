"""test1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from sign_and_auth import views as app_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app_views.index),
    path('logging', app_views.checkLogin),
    path('sign_in',app_views.index),
    path('sign_up', app_views.getAccount),
    path('sign_up_step_two', app_views.signUpData),
    path('sign_up_finish', app_views.finishSignUp),
    path('error',app_views.errorPage)

]
