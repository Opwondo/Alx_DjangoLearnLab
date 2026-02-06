from django.db import models

# Create your models here.

class Author(models.Model):
    """
    Author model representing a book author.
    Each author can have multiple books (one-to-many relationship).
    
    Fields:
    - name: a string field to store the author's name
    """
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Book(models.Model):
    """
    Book model representing a published book.
    
    Fields:
    - title: a string field for the book's title
    - publication_year: an integer field for the year the book was published
    - author: a foreign key linking to the Author model,
              establishing a one-to-many relationship from Author to Books
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
        ordering = ['title']
