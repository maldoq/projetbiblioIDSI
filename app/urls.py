from django.urls import path
from django.conf.urls import handler404
from . import views

urlpatterns = [
    path('', views.signin, name="signin"),
    path('logout/', views.logout_view, name="logout"),
    path('dashboard/', views.dash, name="dashboard"),
    path('api/authors/search/', views.search_authors, name='search_authors'),
    path('api/publishers/search/', views.search_publishers, name='search_publishers'),
    path('books/', views.books_list, name="books_list"),
    path("books/export/excel/", views.books_export_excel, name="books_export_excel"),
    path("books/import/excel/", views.books_import_excel, name="books_import_excel"),
    path('books/add/', views.books_form, name="books_form"),
    path("books/edit/<int:pk>/", views.books_form, name="books_edit"),
    path("books/delete/<int:pk>/", views.books_delete, name="books_delete"),
    path('loans/', views.loans_list, name="loans_list"),
    path('loans/add/', views.loans_form, name="loans_form"),
    path('loans/edit/<int:pk>/', views.loans_form, name="loans_edit"),
    path('loans/delete/<int:pk>/', views.loans_delete, name="loans_delete"),
    path('users/', views.users_list, name="users_list"),
    path('users/export/excel/', views.users_export_excel, name="users_export_excel"),
    path('users/import/excel/', views.users_import_excel, name="users_import_excel"),
    path('users/add/', views.users_form, name="users_form"),
    path('users/edit/<str:pk>/', views.users_form, name="users_edit"),
    path('users/delete/<str:pk>/', views.users_delete, name="users_delete"),
    path('categories/', views.categories_list, name="categories_list"),
    path("categories/add/", views.categories_form, name="categories_form"),
    path("categories/edit/<int:pk>/", views.categories_form, name="categories_edit"),
    path("categories/delete/<int:pk>/", views.categories_delete, name="categories_delete"),
    path('returns_form/', views.returns_form, name="returns_form"),
    path('history/', views.history, name="history"),
    path('history_export/', views.history_export, name="history_export"),
    path('profile/', views.profile, name="profile"),
    path('change_password/', views.change_password, name="change_password"),
]

handler404 = "app.views.custom_404"
