from django.db import models

class Author(models.Model):
    """
    Author model representing a book author.
    Each author can have multiple books (one-to-many relationship).
    """
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']  # Default ordering by author name


class Book(models.Model):
    """
    Book model representing a published book.
    Each book has one author (foreign key relationship).
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE,  # If author is deleted, delete their books
        related_name='books'  # Access books via author.books
    )
    
    def __str__(self):
        return f"{self.title} ({self.publication_year})"
    
    class Meta:
        ordering = ['title']  # Default ordering by book title