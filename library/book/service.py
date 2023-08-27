from django_filters import rest_framework as filters, DateFilter

from .models import Book


class BookFilter(filters.FilterSet):

    class Meta:
        model = Book
        fields = ['genre', 'author', 'published_date']