from rest_framework import serializers

from .models import Book, Review, BookRating


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("name", "genre", "author", "average_rating")


class ReviewCreateSeriaizer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class RecursiveSeriaizer(serializers.Serializer):

    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class FilterReviewListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class ReviewSerializer(serializers.ModelSerializer):
    children = RecursiveSeriaizer(many=True)
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)


    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ("user", "text", "children")


class BookRatingCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookRating
        fields = ("book", "rating", "user")


class BookDetailSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(slug_field="name", read_only=True)
    author = serializers.SlugRelatedField(slug_field="name", read_only=True)
    reviews = ReviewSerializer(many=True)
    average_rating = serializers.ReadOnlyField()

    class Meta:
        model = Book
        fields = "__all__"
