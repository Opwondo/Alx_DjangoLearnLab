
# Advanced API Project – Task 1

## Book API Views

This project implements CRUD operations for the Book model using
Django REST Framework generic views.

## Endpoints

| Method | Endpoint | Description | Access |
|------|---------|-------------|--------|
| GET | /api/books/ | List all books | Public |
| GET | /api/books/<id>/ | Retrieve one book | Public |
| POST | /api/books/create/ | Create book | Authenticated |
| PUT/PATCH | /api/books/<id>/update/ | Update book | Authenticated |
| DELETE | /api/books/<id>/delete/ | Delete book | Authenticated |

## Permissions

- Read operations are open to all users.
- Write operations require authentication.

## Notes

- Uses DRF generic views for cleaner code.
- Validation is handled at serializer level.
