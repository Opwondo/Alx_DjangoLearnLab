from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from api.models import Author, Book


class BookAPITestCase(APITestCase):
    """
    Test suite for Book API endpoints.
    Covers CRUD operations, filtering, searching,
    ordering, and permission enforcement.
    """

    def setUp(self):
        """
        Create initial test data:
        - User for authentication
        - Author
        - Sample books
        """
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

        self.author = Author.objects.create(name="Test Author")

        self.book1 = Book.objects.create(
            title="Django for Beginners",
            publication_year=2021,
            author=self.author
        )

        self.book2 = Book.objects.create(
            title="Advanced Django",
            publication_year=2023,
            author=self.author
        )

        self.list_url = "/api/books/"
        self.create_url = "/api/books/create/"

    # -------------------------
    # READ TESTS
    # -------------------------
    def test_list_books(self):
        """Anyone can list books"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_single_book(self):
        """Anyone can retrieve a single book"""
        url = f"/api/books/{self.book1.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book1.title)

    # -------------------------
    # CREATE TESTS
    # -------------------------
    def test_create_book_unauthenticated(self):
        """Unauthenticated users cannot create books"""
        data = {
            "title": "Unauthorized Book",
            "publication_year": 2022,
            "author": self.author.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_authenticated(self):
        """Authenticated users can create books"""
        self.client.login(username="testuser", password="testpass123")
        data = {
            "title": "New Book",
            "publication_year": 2022,
            "author": self.author.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    # -------------------------
    # UPDATE TESTS
    # -------------------------
    def test_update_book(self):
        """Authenticated users can update a book"""
        self.client.login(username="testuser", password="testpass123")
        url = f"/api/books/update/{self.book1.id}/"
        data = {
            "title": "Updated Django Book",
            "publication_year": 2021,
            "author": self.author.id
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Django Book")

    # -------------------------
    # DELETE TESTS
    # -------------------------
    def test_delete_book(self):
        """Authenticated users can delete a book"""
        self.client.login(username="testuser", password="testpass123")
        url = f"/api/books/delete/{self.book1.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    # -------------------------
    # FILTERING TESTS
    # -------------------------
    def test_filter_books_by_year(self):
        """Filter books by publication year"""
        response = self.client.get(self.list_url + "?publication_year=2023")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # -------------------------
    # SEARCH TESTS
    # -------------------------
    def test_search_books(self):
        """Search books by title"""
        response = self.client.get(self.list_url + "?search=Advanced")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # -------------------------
    # ORDERING TESTS
    # -------------------------
    def test_order_books_by_year_desc(self):
        """Order books by publication year descending"""
        response = self.client.get(self.list_url + "?ordering=-publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[0]["publication_year"],
            2023
        )
