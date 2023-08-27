from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    """Жанры"""
    name = models.CharField("Имя", max_length=100)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Author(models.Model):
    """Авторы"""
    name = models.CharField('Автор', max_length=100)
    about = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class Book(models.Model):
    """ Книга """
    name = models.CharField(max_length=100)
    published_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    ISBN = models.IntegerField(null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)


    @property
    def average_rating(self):
        # get all the BookRatingModel from the database
        ratings = BookRating.objects.filter(book=self.id)
        if len(ratings) > 0:
            return sum([x.rating for x in ratings]) / len(ratings)
        else:
            return 0

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"


class BookRating(models.Model):
    """Рейтинг"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)

    class Meta:
        unique_together = ["book", "user"]

    def __str__(self):
        return f"Book \"{self.book.name}\"  rated {self.rating} by User {self.user.username}"


class Review(models.Model):
    """Отзывы"""

    text = models.TextField("Сообщение", max_length=5000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True, related_name="children"
    )
    book = models.ForeignKey(Book, verbose_name="книга", on_delete=models.CASCADE, related_name="reviews")

    def __str__(self):
        return f"{self.user} - {self.book}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
