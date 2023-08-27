from django.urls import path

from . import views

urlpatterns = [
    path("book/", views.BookListView.as_view()),
    path("book/<int:pk>/", views.BookDetailView.as_view()),
    path("review/", views.ReviewCreateView.as_view()),
    path("rating/", views.BookRatingCreateView.as_view()),
]