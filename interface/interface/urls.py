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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', GenericModelView.as_view(), name='index'),
    path('firstname/', GenericModelView.as_view(),{'model_name': 'firstname'}, name='firstname_list'),
    path('delete_task/<int:task_id>/', delete_task, name='delete_task'),
    path('add_edit_task/', LineCreateView.as_view(), name='add_edit_task'),
    path('edit_task/<int:id>/', LineUpdateView.as_view(), name='edit_task'),
    path('search/', SearchView.as_view(), name='search')

]
