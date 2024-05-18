from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('log-in/', views.log_in, name='log_in'),
    path('log-out/', views.log_out, name='log_out'),
    # Category
    path('category-create/', views.category_create, name='category_create'),
    path('category-update/<str:code>/', views.category_update, name='category_update'),
    path('category-list/', views.category_list, name='category_list'),
    path('category-delete/<str:code>/', views.category_delete, name='category_delete'),
    # Product
    path('product-create/', views.product_create, name='product_create'),
    path('product-list/', views.product_list, name='product_list'),
    path('product-delete/<str:code>/', views.product_delete, name='product_delete'),
    path('product-update/<str:code>/', views.product_update, name='product_update'),
    # Entery
    path('entry-create/', views.entry_create, name='entry_create'),
    path('entry-list/', views.entry_list, name='entry_list'),
    # Outery
    path('outery-create/', views.outery_create, name='outery_create'),
    path('outery-list/', views.outery_list, name='outery_list'),
    # Return
    path('return-create/', views.return_create, name='return_create'),
    path('return-list/', views.return_list, name='return_list'),


]
