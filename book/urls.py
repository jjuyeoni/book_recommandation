from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('search', views.search, name='search'),
    path('mybook/<num>', views.mybook, name='mybook'),
    path('detail/<title>', views.detail, name='detail'),
    path('b_search', views.b_search, name='b_search'),

    path('bAjax', views.bAjax, name='bs'),
]
