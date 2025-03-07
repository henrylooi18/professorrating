"""professor_rating URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from ratings.views import (ModuleInstanceList, ProfessorRating, ProfessorModuleRating, RateProfessor, RegisterUser, LoginUser, LogoutUser, main)

urlpatterns = [
    path('', main, name='home'),
    path('admin/', admin.site.urls),
    path('list/', ModuleInstanceList.as_view(), name='module-instance-list'),
    path('view/', ProfessorRating.as_view(), name='view-professor-ratings'),
    path('average/<str:professor_code>/<str:module_code>/', ProfessorModuleRating.as_view(), name='average-professor-module-rating'),
    path('rate/', RateProfessor.as_view(), name='rate-professor'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
]
