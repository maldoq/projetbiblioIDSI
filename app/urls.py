from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.signin, name="signin"),
    path('/dashboard', views.dash, name="dashboard"),
    path('/books', views.books_list, name="books_list"),
    path('/loans', views.loans_list, name="loans_list"),
    path('/users', views.users_list, name="users_list"),
    path('/categories', views.categories_list, name="categories_list"),
    path('/loans_form', views.loans_form, name="loans_form"),
    path('/returns_form', views.returns_form, name="returns_form"),
    path('/books_form', views.books_form, name="books_form"),
    path('/users_form', views.users_form, name="users_form"),
    path('/categories_form', views.categories_form, name="categories_form"),
    path('/history', views.history, name="history"),
    path('/history_export', views.history_export, name="history_export"),
    path('/profile', views.profile, name="profile"),
    path('/change_password', views.change_password, name="change_password"),
    path('/logout', views.logout, name="logout"),
]
