"""scraping_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from scraping.views import (
    home_view, list_view, vacancy_detail,
    VacancyDetail, VacancyList, VacancyCreateView,
    VacancyUpdateView, VacancyDelete)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('list', VacancyList.as_view(), name='list'),
    path('accounts/', include(('accounts.urls', 'accounts'))),
    path('detail/<int:pk>/', VacancyDetail.as_view(), name='detail_vacancy'),
    path('create/', VacancyCreateView.as_view(), name='create'),
    path('update/<int:pk>/', VacancyUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', VacancyDelete.as_view(), name='delete'),

    # path('scraping/', include('scraping.urls'))
]
