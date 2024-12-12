from django.db import models
from django.core.exceptions import ValidationError

class Author(models.Model):
    name = models.CharField(max_length=100)
    biography = models.TextField()

    def __str__(self):
        return self.name

class Book(models.Model):
    BOOK_TYPES = (
        ('fiction', 'Художественное произведение'),
        ('textbook', 'Учебник'),
    )
    
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    publication_year = models.IntegerField()
    genre = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100) 
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    file = models.FileField(upload_to='books/', blank=True, null=True)
    book_type = models.CharField(max_length=10, choices=BOOK_TYPES, default='fiction')

    class Meta:
        unique_together = ('title', 'author', 'publication_year', 'publisher')

    def save(self, *args, **kwargs):

        if self.book_type == 'fiction':
            existing_fiction_books = Book.objects.filter(
                title=self.title,
                author=self.author,
                publisher=self.publisher, 
                book_type='fiction'
            ).exclude(id=self.id)

            if existing_fiction_books.exists():
                raise ValidationError("Художественное произведение с таким названием и автором уже существует для данного издательства.")#надо поменять только издательство чтобы была ошибка
            
        # Проверка на уникальность учебников
        if self.book_type == 'textbook':
            existing_textbooks = Book.objects.filter(
                title=self.title,
                author=self.author,
                publication_year=self.publication_year,
                book_type='textbook'
            ).exclude(id=self.id)

            if existing_textbooks.exists():
                raise ValidationError("Учебник с таким названием и автором уже существует для данного года публикации.")#надо поменять только год издания чтобы была ошибка
        

        super().save(*args, **kwargs)

  
