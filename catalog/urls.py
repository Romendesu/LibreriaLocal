from django.urls import path, re_path
from . import views

# Rutas para catalog
urlpatterns = [
    # Index
    path('', views.index, name= 'index'),

    # Rutas para los libros y los autores
    path('books/', views.BookListView.as_view(), name="books"),
    path('author/', views.AuthorListView.as_view(), name="author"),

    # Rutas para el detalle de los libros y los autores
    re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
    re_path(r'^book/(?P<pk>[-\w]+)/renew/$', views.renew_book_librarian, name='renew-book-librarian'),
    re_path(r'^author/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    
]

urlpatterns += [
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
]