"""
URL configuration for interface project.

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




from phone_directory.views import GenericModelView, delete_task, LineCreateView, LineUpdateView, SearchView
from phone_directory.models import Main, Firstname, Street, Surname, Patronymic
from phone_directory.forms import MainForm, FirstnameForm, StreetForm, SurnameForm, PatronymicForm



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', GenericModelView.as_view(), name='main_list'),
    path('firstname/', GenericModelView.as_view(),{'model_name': 'firstname'}, name='firstname_list'),
    path('surname/', GenericModelView.as_view(),{'model_name': 'surname'}, name='surname_list'),
    path('street/', GenericModelView.as_view(),{'model_name': 'street'}, name='street_list'),
    path('patronymic/', GenericModelView.as_view(),{'model_name': 'patronymic'}, name='patronymic_list'),
    path('delete_task/<slug:model_name>/<int:task_id>/', delete_task, name='delete_task'),
    path('edit_task/<int:id>/', LineUpdateView.as_view(), name='edit_task'),
    path('search/', SearchView.as_view(), name='search'),
    path('main_create/', LineCreateView.as_view(), name='main_create'),
    path('firstname_create/', LineCreateView.as_view(),{'model_name': 'firstname'}, name='firstname_create'),
    path('surname_create/', LineCreateView.as_view(),{'model_name': 'surname'}, name='surname_create'),
    path('street_create/', LineCreateView.as_view(),{'model_name': 'street'}, name='street_create'),
    path('patronymic_create/', LineCreateView.as_view(),{'model_name': 'patronymic'}, name='patronymic_create'),

]
