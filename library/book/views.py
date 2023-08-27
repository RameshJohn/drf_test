from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend

from .service import BookFilter

from .models import Book
from .serializers import (
    BookListSerializer,
    BookDetailSerializer,
    ReviewCreateSeriaizer,
    BookRatingCreateSerializer)


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BookFilter
    serializer_class = BookListSerializer


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewCreateSeriaizer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookRatingCreateView(generics.CreateAPIView):
    serializer_class = BookRatingCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
