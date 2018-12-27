from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('search', views.search, name='search'),
    path('mybook/<num>', views.mybook, name='mybook'),
    path('detail/<title>', views.detail, name='detail'),
]
