"""myweb URL Configuration

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
from django.urls import path
from user.views import CreateUserView, UserListView, LoginView, LogoutView
from personalexpense.views import ExpenseCreateView, ExpenseUpdateDeleteView,ExpenseListView, ExpenseDetailView, ExpenseCloneView, ExpenseShortURLView, ExpenseShortURLDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', CreateUserView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='users'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('expenses/create/', ExpenseCreateView.as_view(), name='expense-create'),
    path('expenses/<int:pk>/', ExpenseUpdateDeleteView.as_view(), name='expense-update-delete'),
    path('expenses/', ExpenseListView.as_view(), name='expense-list'),
    path('expenses/detail/<int:pk>/', ExpenseDetailView.as_view(), name='expense-detail'),
    path('expenses/clone/<int:pk>/', ExpenseCloneView.as_view(), name='expense-clone'),
    path('expenses/short_url/<int:pk>/', ExpenseShortURLView.as_view(), name='expense-short-url'),
    path('s/<str:short_url>/', ExpenseShortURLDetailView.as_view(), name='expense-detail-short-url'),
]
